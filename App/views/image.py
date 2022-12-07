from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, send_from_directory
from flask_jwt import jwt_required
from flask_login import login_required, current_user


from App.controllers import (
    create_image, 
    get_all_images,
    get_all_images_json,
    get_images_by_userid_json,
    get_image,
    get_image_json,
    delete_image,
    get_user
)

image_views = Blueprint('image_views', __name__, template_folder='../templates')


@image_views.route('/uploadImage', methods=['GET'])
@login_required
def get_image_page():
    images = get_all_images()
    return render_template('upload.html')

@image_views.route('/uploadImage', methods=['POST'])
@login_required
def uploadImageAction():
    data = request.form
    uploadImage = create_image(current_user.id, data['url'])
    flash("Image Uploaded!")
    return render_template('homePage.html')

@image_views.route('/createImage/<user>', methods=['POST'])
def create_image_action(user):
    data = request.json
    user = get_user(user)
    if user:
        image = create_image(user, data['url'])
        return jsonify({"message":"Image created"}) 
    return jsonify({"message":"User does not exist"}) 

@image_views.route('/allImages', methods=['GET'])
@login_required
def get_images_all_action():
    images = get_all_images()
    return render_template('images.html', images=images)

@image_views.route('/api/images/user/<int:id>', methods=['GET'])
def get_images_by_user_action(id):
    images = get_images_by_userid_json(id)
    if not picture:
        return jsonify({'message':'ERROR: Picture not found'}),404
    return jsonify({'picture': picture.toJSON()}), 200

@image_views.route('/api/images/<int:id>', methods=['GET'])
def get_images_by_id_action(id):
    image = get_image_json(id)
    if not picture:
        return jsonify({'message':'ERROR: Picture not found'}), 404
    return jsonify({'picture': picture.toJSON()}), 200

@image_views.route('/api/addImage', methods=['POST'])
def create_image_Fun():
    data = request.json
    user = get_user(data['user'])
    if user:
        image = create_image(data['user'], data['url'])
        return jsonify({"message":"Image created"}) 
    return jsonify({"message":"User does not exist"}) 

@image_views.route('/deleteImage/<int:id>', methods=['DELETE'])
@login_required
def delete_image_action(id):
    if get_image(id):
        delete_image(id)
        return jsonify({"message":"Image Deleted"}), 200
    return jsonify({'message':'ERROR: Picture not found'}), 404 
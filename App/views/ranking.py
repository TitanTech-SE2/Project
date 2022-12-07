from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash
from flask_jwt import jwt_required
from flask_login import login_required, current_user

from App.controllers import (
    create_ranking, 
    get_all_rankings,
    get_all_rankings_json,
    get_ranking,
    get_rankings_by_image,
    get_rankings_by_creator,
    get_ranking_by_actors,
    get_calculated_ranking,
    update_ranking,
    get_user,
    get_image
)

ranking_views = Blueprint('ranking_views', __name__, template_folder='../templates')

@ranking_views.route('/api/rankings', methods=['POST'])
def create_ranking_action():
    data = request.json
    if get_user(data['creatorId']) and get_image(data['imageId']):
        image = get_image(data['imageId'])
        if data['creatorId'] != image.user:

            prev = get_ranking_by_actors(data['creatorId'], data['imageId'])
            if prev:
                return jsonify({"message":"Current user already ranked this image"}) 
            ranking = create_ranking(data['creatorId'], data['imageId'], data['score'])
            return jsonify({"message":"Ranking created"}) 

        return jsonify({"message":"User cannot rank self"})
    return jsonify({"message":"User not found"}) 

@ranking_views.route('/ranking/<int:imageID>', methods=['POST'])
@login_required
def set_ranking_action(imageID):

    data = request.form

    existingRank = get_ranking_by_actors(current_user.id, imageID)

    if not existingRank:
        ranking = create_ranking(current_user.id, imageID, data['score'])
    else: 
        update_ranking(existingRank.id, data['score'])

    flash(f"Saved rating of  {data['score']}  on  {imageID} ")
    return render_template('homePage.html')


    # request.get_json(force=True)
    # data = request.form
    # image = request.form.image
    # update_ranking(data.id, data.score)
    # if get_user(current_user.id) and get_image(data.id):
    #     image = get_image(data.id)
    #     if current_user.id != image.user:

    #         prev = get_ranking_by_actors(current_user.id, data.id)
    #         if prev:
    #             return render_template(images.html)
                
    # ranking = create_ranking(current_user.id, data['id'], data['score'])
        #     return render_template(images.html)

        # return render_template(images.html)
    # return render_template(images.html)

@ranking_views.route('/api/rankings', methods=['GET'])
def get_all_rankings_action():
    rankings = get_all_rankings_json()
    return jsonify(rankings)

@ranking_views.route('/api/rankings/byid/<int:id>', methods=['GET'])
def get_ranking_action(id):
    ranking = get_ranking(id)
    if ranking:
        return ranking.toJSON()
    return jsonify({"message":"Ranking Not Found"})

@ranking_views.route('/api/rankings/bycreator/<int:id>', methods=['GET'])
def get_rankings_by_creator_action(id):
    if get_user(id):
        ranking = get_rankings_by_creator(id)
        if ranking:
            return jsonify(ranking)
    return jsonify({"message":"User Not Found"})

@ranking_views.route('/api/rankings/byimage/<int:id>', methods=['GET'])
def get_rankings_by_image_action(id):
    if get_image(id):
        ranking = get_rankings_by_image(id)
        if ranking:
            return jsonify(ranking)
    return jsonify({"message":"Image Not Found"})

@ranking_views.route('/api/rankings', methods=['PUT'])
def update_ranking_action():
    data = request.json
    ranking = update_ranking(data['id'], data['score'])
    if ranking:
        return jsonify({"message":"Ranking updated"})
    return jsonify({"message":"Ranking not found"})


@ranking_views.route('/api/rankings/calc/<int:id>', methods=['GET'])
def get_calculated_ranking_action(id):
    if get_image(id):
        ranking = get_calculated_ranking(id)
        if ranking:
            return jsonify({"calculated_ranking": ranking}) 
        return jsonify({"message":"No rankings by this image found"})
    return jsonify({"message":"Image not found"})
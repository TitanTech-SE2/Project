from flask import Blueprint, render_template, jsonify, request, send_from_directory, redirect, url_for, Flask, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_jwt import current_identity, jwt_required
from werkzeug.utils import secure_filename
#from webforms import LoginForm, UserForm, PasswordForm, SearchForm, UploadForm
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import date
from datetime import datetime

from App.controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
    get_user,
    get_user_by_username,
    update_user,
    delete_user,
    login_user,
    logout_user,
    get_level,
    authenticate,
    identity,
    get_images_by_userid,
    getTotalRatings
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.errorhandler(404)
def page_not_found(code):
    return render_template('404.html'), 404

@user_views.route('/api/newUser', methods=['POST'])
def create_user_action():
    data = request.json
    user = get_user_by_username(data['username'])
    if user:
        return jsonify({"message":"Username Already Taken"}) 
    user = create_user(data['username'], data['password'])
    return jsonify({"message":"User Created"}) 

@user_views.route('/signup',methods=['GET'])
def showSignUp():
    return render_template('signupPage.html')

@user_views.route('/signup',methods=['POST'])
def userSignUP():
    data = request.form
    user = get_user_by_username(data['username'])
    if user:
        flash("Sorry! Username exists in database already")
        return showSignUp()
    user = create_user(data['username'], data['password'])
    return showLogin()


@user_views.route('/home',methods=['GET'])
@login_required
def get_homePage():
    flash(" Get ready to start voting "+current_user.username + " !")
    return render_template('homePage.html')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users', methods=['GET'])
def get_all_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users/level/<int:id>', methods=['GET'])
def get_user_action(id):
    data = request.form
    user = get_user(id)
    if user:
        return user.toJSON() 
    return jsonify({"message":"User Not Found"})

@user_views.route('/api/users', methods=['PUT'])
def update_user_action():
    data = request.form
    user = update_user(data['id'], data['username'])
    if user:
        return jsonify({"message":"User Updated"})
    return jsonify({"message":"User Not Found"})
    

@user_views.route('/auth',methods=['GET'])
def showLogin():
    return render_template('loginPage.html')

@user_views.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user_action(id):
    if get_user(id):
        delete_user(id)
        return jsonify({"message":"User Deleted"}) 
    return jsonify({"message":"User Not Found"}) 

@user_views.route('/auth',methods=['POST'])
def loginAction():
    data=request.form
    user =authenticate(data['username'], data['password'])
    if user == None:
        flash("Username and password do not match")
        return showLogin(), jsonify({"message":"Username and password do not match"}) 
    login_user(user,remember=True)
    return get_homePage()

@user_views.route("/logout")
@login_required
def userLogout():
    logout_user()
    return render_template("index.html")

@user_views.route('/api/users/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"username: {current_identity.username}, id : {current_identity.id}"})
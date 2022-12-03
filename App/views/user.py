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
    update_profile_pic
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.errorhandler(404)
def page_not_found(code):
    return render_template('404.html'), 404

""" @user_views.route('/signup',methods=['GET', 'POST']) #commenting this out to fix errors
def showSignUp():
    userName = None
    form = UserForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user:
		flash("Sorry! Username exists in database already")
        	return showSignUp()

	else:
		user = create_user(form.username.data, form.password.data)
        
	userName = form.username.data
        form.username.data = ''
	form.password.data = ''
        flash("User Added Successfully")
                
    return render_template('signupPage.html', form = form, userName = userName) """
    
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
@login_required
def get_user_action(id):
    data = request.form
    user = get_user(id)
    if user:
        return user.toJSON() 
    return jsonify({"message":"User Not Found"})

@user_views.route('/api/users', methods=['PUT'])
@login_required
def update_user_action():
    data = request.form
    user = update_user(data['id'], data['username'])
    if user:
        return jsonify({"message":"User Updated"})
    return jsonify({"message":"User Not Found"})
    

""" @app.route('/App/Uploads/<filename>') #use urls instead of files
def getFile(filename):
	   return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename) """


""" @app.route('/user/upload', methods = ['GET', 'POST']
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
	   filename = photos.save(form.photo.data)
	   file_url = url_for('getFile', filename=filename)
    else:
	   file_url = None
	   
    return render_template('upload.html', form = form, file_url = file_url) """



@user_views.route('/auth',methods=['GET'])
def showLogin():
    return render_template('loginPage.html')

@user_views.route('/api/users/<int:id>', methods=['DELETE'])
@login_required
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

@user_views.route('/newuser',methods=['POST'])
def makeUser():
    data = request.json
    user = get_user_by_username(data['username'])
    if user:
        return jsonify({"message":"Sorry! Username exists in database already"}) 
    user = create_user(data['username'], data['password'])
    return jsonify({"message":"User Created"}) 


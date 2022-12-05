from flask_jwt import jwt_required, current_identity
from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_login import current_user, login_required

from App.controllers import (
    createNewDistributor,
    GenerateFeed,
    get_all_users
)

distributor_views = Blueprint('distributor_views', __name__, template_folder='../templates')

@distributor_views.route('/createNewDistributor',methods=['GET'])
#@jwt_required()
def createDistributor():
    users = get_all_users()
    NewDistributor = createNewDistributor(len(users))
    return jsonify({"message":"Distributor has been created!"})

@distributor_views.route('/feed', methods=['GET'])
@login_required
def feed():
    users = get_all_users()
    users=GenerateFeed(sender=current_identity.id)
    return render_template('feed.html', profilesToShow=users)
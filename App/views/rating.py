from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required


from App.controllers import (
    create_rating, 
    get_all_ratings,
    get_all_ratings_json,
    get_rating,
    get_ratings_by_target,
    get_ratings_by_creator,
    get_rating_by_actors,
    update_rating,
    get_user,
    getTotalRatings,
    get_calculated_rating
)

rating_views = Blueprint('rating_views', __name__, template_folder='../templates')


@rating_views.route('/api/ratings', methods=['POST'])
def create_rating_action():
    data = request.json
    if get_user(data['creatorId']) and get_user(data['targetId']):
        if data['creatorId'] != data['targetId']:
            
            prev = get_rating_by_actors(data['creatorId'], data['targetId'])
            if prev:
                return jsonify({"message":"Current user already rated this user"}) 
            rating = create_rating(data['creatorId'], data['targetId'], data['score'])
            return jsonify({"message":"Rating created"}) 

        return jsonify({"message":"User cannot rate self"})
    return jsonify({"message":"User not found"}) 

@rating_views.route('/api/ratings', methods=['GET'])
def get_all_ratings_action():
    ratings = get_all_ratings_json()
    return jsonify(ratings)

@rating_views.route('/api/ratings/byid/<int:id>', methods=['GET'])
def get_rating_action(id):
    rating = get_rating(id)
    if rating:
        return rating.toJSON()
    return jsonify({"message":"Rating not found"})

@rating_views.route('/api/ratings/bycreator/<int:id>', methods=['GET'])
def get_rating_by_creator_action(id):
    if get_user(id):
        rating = get_ratings_by_creator(id)
        if rating:
            return jsonify(rating) 
        return jsonify({"message":"No ratings by this user found"})
    return jsonify({"message":"User not found"})

@rating_views.route('/api/ratings/bytarget/<int:id>', methods=['GET'])
def get_rating_by_target_action(id):
    if get_user(id):
        rating = get_ratings_by_target(id)
        if rating:
            return jsonify(rating) 
        return jsonify({"message":"No ratings for this user found"})
    return jsonify({"message":"User not found"})

@rating_views.route('/api/ratings', methods=['PUT'])
def update_rating_action():
    data = request.json
    rating = update_rating(data['id'], data['score'])
    if rating:
        return jsonify({"message":"Rating updated"})
    return jsonify({"message":"Rating not found"})

@rating_views.route('/api/ratings/total', methods=['GET'])
def showTotalRatings():
    ratings = getTotalRatings()
    return (str(ratings))

@rating_views.route('/api/ratings/calc/<int:id>', methods=['GET'])
def get_calculated_rating_action(id):
    if get_user(id):
        rating = get_calculated_rating(id)
        if rating:
            return jsonify({"calculated rating": rating}) 
        return jsonify({"message":"No ratings by this user found"})
    return jsonify({"message":"User not found"})
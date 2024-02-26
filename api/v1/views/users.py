#!/usr/bin/python3
""" view for User objects that handles all default RESTFul API actions """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ list all User objects """
    users = storage.all('User').values()
    users = [user.to_dict() for user in users]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ get User object with the given id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ delete User object """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    try:
        for place in user.places:
            for review in place.reviews:
                storage.delete(review)
            storage.delete(place)
        for review in user.reviews:
            storage.delete(review)
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """ Create User """
    query_parameters = request.get_json(silent=True, force=True)
    if not query_parameters:
        abort(400, "Not a JSON")
    if 'email' not in query_parameters:
        abort(400, "Missing email")
    if 'password' not in query_parameters:
        abort(400, "Missing password")
    user = User(**query_parameters)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Updates User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    changes = request.get_json(silent=True, force=True)
    if not changes:
        abort(400, "Not a JSON")
    try:
        for key, value in changes.items():
            if key in ['password', 'first_name', 'last_name']:
                setattr(user, key, value)
        user.save()
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500
    return jsonify(user.to_dict()), 200

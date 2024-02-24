#!/usr/bin/python3
""" view for User objects that handles all default RESTFul API actions """
from flask import Flask, request, jsonify
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users',
                 strict_slashes=False)
def get_users():
    """ list all User objects """
    users = storage.all('User').values()
    users = [user.to_dict() for user in users]
    return jsonify(users)


@app_views.route('/users/<user_id>',
                 strict_slashes=False)
def get_user(user_id):
    """ get User object with the given id """
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ delete User object """
    user = storage.get(User, user_id)
    print(user)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    try:
        for place in user.places:
            storage.delete(place)
        for review in user.reviews:
            storage.delete(review)
        storage.delete(user)
        storage.save()
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"}), 500
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """ Create User """
    try:
        obj = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in obj:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in obj:
        return jsonify({"error": "Missing password"}), 400
    user = User(**obj)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Updates User object """
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    try:
        changes = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in changes.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    try:
        user.save()
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500
    return jsonify(user.to_dict()), 200

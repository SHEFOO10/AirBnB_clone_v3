#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""
from flask import Flask, request, abort, jsonify
from api.v1.views import app_views
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all cities in state"""
    state = storage.get('State', state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())

    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object by id"""
    city = storage.get('City', city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object by ID"""
    city = storage.get('City', city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    for place in city.places:
        place.delete()
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def add_city_to_state(state_id):
    """adding city"""
    state = storage.get('State', state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    try:
        req = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in req:
        return jsonify({"error": "Missing name"}), 400
    city = City(**req)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """changes in city"""
    city = storage.get('City', city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    try:
        for key, value in request.get_json().items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    city.save()
    return jsonify(city.to_dict()), 200

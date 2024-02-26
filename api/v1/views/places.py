#!/usr/bin/python3
""" a view for Place objects that handles all default RESTFul API actions """
from flask import request, jsonify
from api.v1.views import app_views
from models.place import Place
from models import storage


@app_views.route('cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get('City', city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    places = [place.to_dict() for place in city.places]
    return jsonify(places), 200


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """ Retrieves a Place object. """
    place = storage.get('Place', place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get('Place', place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """ Creates a Place """
    city = storage.get('City', city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    query_parameters = request.get_json(force=True, silent=True)
    if not query_parameters:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in query_parameters:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get('User', query_parameters.get('user_id'))
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if 'name' not in query_parameters:
        return jsonify({"error": "Missing name"}), 400
    query_parameters.update({"city_id": city_id})
    new_place = Place(**query_parameters)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get('Place', place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    changes = request.get_json(force=True, silent=True)
    if not changes:
        return jsonify({"error": "Not a JSON"}), 400
    print(changes)
    for key, value in changes.items():
        if key in ['name',
                   'description',
                   'number_rooms',
                   'number_bathrooms',
                   'max_guest',
                   'price_by_night',
                   'latitude',
                   'longitude',
                   ]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

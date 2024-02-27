#!/usr/bin/python3
"""
    a view for the link between Place objects
    and Amenity objects that handles all default RESTFul API
"""
from flask import request, abort, jsonify
from models.amenity import Amenity
from models.place import Place
from models import storage, storage_t
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
def get_place_amenities(place_id):
    """ Retrieves the list of all Amenity objects of a Place """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if storage_t != 'db':
        amenities = [storage.get('Amenity', amenity).to_dict()
                     for amenity in place.amenities]
    else:
        amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(place_id, amenity_id):
    """ Remove a Amenity object link to a Place """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    new_amenities_list = []
    found = False
    if storage_t != 'db':
        for place_amenity_id in place.amenity_ids:
            if place_amenity_id != amenity_id:
                new_amenities_list.append(amenity.to_dict())
            else:
                found = True
        if found is False:
            abort(404)
        place.amenity_ids = new_amenities_list
    else:
        for amenity in place.amenities:
            if amenity.id != amenity_id:
                new_amenities_list.append(amenity)
            else:
                found = True
        if found is False:
            abort(404)
        place.amenities = new_amenities_list
    place.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def place_amenity(place_id, amenity_id):
    """ Link amenity to place """
    place = storage.get('Place', place_id)
    print("place: ", place)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if storage_t != 'db':
        found = False
        amenities = place.amenity_ids
        for place_amenity in place.amenity_ids:
            if place_amenity == amenity_id:
                found = True
        if found is False:
            amenities.append(amenity_id)
            place.amenity_ids = amenities
    else:
        found = False
        for place_amenity in place.amenities:
            if place_amenity.id == amenity_id:
                found = True
        if found is False:
            place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201

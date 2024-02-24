#!/usr/bin/python3
"""view for Amenity objects that handles all default RESTFul API actions"""
from flask import Flask, request, abort, jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_aminity():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all('Amenity').values()
    amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object by id"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete(amenity_id):
    """delete amenity by id"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create():
    """ Create Amenity Record """
    try:
        req = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in req:
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**req)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update(amenity_id):
    """Updates a Amenity object by id"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404

    try:
        req = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in req.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200

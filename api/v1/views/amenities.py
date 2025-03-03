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
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete(amenity_id):
    """delete amenity by id"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create():
    """ Create Amenity Record """
    req = request.get_json(silent=True, force=True)
    if not req:
        abort(400, "Not a JSON")
    if 'name' not in req:
        abort(400, "Missing name")
    amenity = Amenity(**req)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update(amenity_id):
    """Updates a Amenity object by id"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    try:
        req = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200

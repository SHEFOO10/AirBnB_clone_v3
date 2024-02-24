#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""
from flask import Flask, request, jsonify
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State"""
    states = storage.all('State').values()
    states = [state.to_dict() for state in states]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_byID(state_id):
    """Retrieves a State object by id"""
    state = storage.get('State', state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state_byID(state_id):
    """Deletes a State object by id"""
    state = storage.get('State', state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    try:
        for city in state.cities:
            for place in city.places:
                storage.delete(place)
            storage.delete(city)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    except Exception as e:
        print("An error occurred during state deletion:", e)
        return jsonify({"error": "Internal server error"}), 500


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a State"""
    try:
        changes = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in changes:
        return jsonify({"error": "Missing name"}), 400
    state = State(**changes)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],  strict_slashes=False)
def update_state(state_id):
    """Updates a State object by id"""
    state = storage.get('State', state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    try:
        changes = request.get_json()
        for key, value in changes.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

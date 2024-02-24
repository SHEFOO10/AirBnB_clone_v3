#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""
from flask import Flask, request, abort, jsonify
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_status():
    """Retrieves the list of all State"""
    states = storage.all('State').values()
    states = [state.to_dict() for state in states]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_byID(state_id):
    """Retrieves a State object by id"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404, "Not found")
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state_byID(state_id):
    """Deletes a State object by id"""
    pass


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a State"""
    pass


@app_views.route('/states/<state_id>', methods=['POST'],  strict_slashes=False)
def update_state(state_id):
    """Updates a State object by id"""
    pass

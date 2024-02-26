#!/usr/bin/python3
"""view for Review object that handles all default RESTFul API"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.review import Review
from models import storage


@app_views.route('places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def get_reviews(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews), 200


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """ Retrieves a Review object """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """ Creates a Review """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    query_parameters = request.get_json(force=True, silent=True)
    if not query_parameters:
        abort(400, "Not a JSON")
    if 'user_id' not in query_parameters:
        abort(400, "Missing user_id")
    user = storage.get('User', query_parameters.get('user_id'))
    if user is None:
        abort(404)
    if 'text' not in query_parameters:
        return abort(400, "Missing text")
    query_parameters.update({"place_id": place_id})
    new_review = Review(**query_parameters)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """ Updates a Review object """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    changes = request.get_json(force=True, silent=True)
    if not changes:
        abort(400, "Not a JSON")
    for key, value in changes.items():
        if key in ['text']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200

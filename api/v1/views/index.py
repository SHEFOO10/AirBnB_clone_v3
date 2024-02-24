#!/usr/bin/python3
"""3. Status of your API"""

from flask import jsonify
from api.v1.views import app_views
from models.engine.db_storage import classes
from models import storage


@app_views.route("/status",
                 strict_slashes=False)
def status():
    """ return the status of The API """
    return jsonify({"status": "OK"})


@app_views.route("/stats",
                 strict_slashes=False)
def stats():
    """ retrieves the number of each objects by type """
    class_plural = {"Amenity": 'amenities',
                    "City": 'cities',
                    "Place": 'places',
                    "Review": 'reviews',
                    "State": 'states',
                    "User": 'users'}
    stats = {}
    for cls_name, cls in classes.items():
        stats.update({class_plural[cls_name]: storage.count(cls)})
    return jsonify(stats)

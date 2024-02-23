#!/usr/bin/python3
"""3. Status of your API"""

from flask import jsonify
from api.v1.views import app_views

@app_views.route("/status",
                 strict_slashes=False)
def status():
    """ return the status of The API """
    return jsonify({"status": "OK"})

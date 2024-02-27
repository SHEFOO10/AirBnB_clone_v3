from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.errorhandler(404)
def not_found(err):
    """ return json error with status code 404 """
    return jsonify({"error": "Not found"}), 404


@app_views.errorhandler(400)
def bad_request(err):
    """ return Bad Request Error with error message """
    return jsonify({"error": err.description}), 400


if __name__ == 'api.v1.views':
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.cities import *
    from api.v1.views.amenities import *
    from api.v1.views.users import *
    from api.v1.views.places import *
    from api.v1.views.places_reviews import *
    from api.v1.views.places_amenities import *

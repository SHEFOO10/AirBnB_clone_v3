#!/usr/bin/pyhton3
"""3. Status of your API"""

from flask import Flask
import os
from models import storage
from api.v1.views import app_views

host = os.environ['HBNB_API_HOST']
port = os.environ['HBNB_API_PORT']

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(error):
    storage.close()


if __name__ == "__main__":
    app.run(port=port, host=host, threaded=True)

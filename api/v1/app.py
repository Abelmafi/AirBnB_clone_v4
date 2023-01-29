#!/usr/bin/python3
"""Api creations"""


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(404)
def not_found(error):
    """Custome 404 error handler"""
    return jsonify({'error': 'Not found'}), 404


@app.teardown_appcontext
def teardown(error):
    """..."""
    storage.close()


if __name__ == '__main__':
    """..."""
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)

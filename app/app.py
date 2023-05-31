import os

from flask import Flask, jsonify, make_response
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt


def custom_response(code, message, data=None):
    response_data = {
        'code': code,
        'message': message,
        'data': data
    }
    response = make_response(jsonify(response_data), code)
    response.headers['Content-Type'] = 'application/json'
    return response


application = Flask(__name__)

application.config["MONGODB_SETTINGS"] = {
#    'db': os.environ['MONGODB_DATABASE'],
#    'host': os.environ['MONGODB_HOSTNAME'],
#    'port': 27017,
#    'username': os.environ['MONGODB_USERNAME'],
#    'password': os.environ['MONGODB_PASSWORD'],
    'db': 'flaskdb', 
    'host': 'localhost',
    'port': 27017,
    'username': 'flask',
    'password': 'flaskpass',
}

db = MongoEngine(application)
ma = Marshmallow(application)
bcrypt = Bcrypt(application)

@application.route('/')
def index():
    return custom_response(200, 'Welcome to blog sample API with flask and mongodb')


from .urls import blueprint 
application.register_blueprint(blueprint)


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)

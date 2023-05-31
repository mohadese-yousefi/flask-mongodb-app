from flask import Blueprint

from .resources import auth


blueprint = Blueprint('users', __name__, url_prefix='/users')
blueprint.register_blueprint(auth.blueprint)

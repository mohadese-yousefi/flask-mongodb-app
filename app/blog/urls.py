from flask import Blueprint

from .resources import post, comment


blueprint = Blueprint('blog', __name__, url_prefix='/blog')
blueprint.register_blueprint(post.blueprint)
blueprint.register_blueprint(comment.blueprint)

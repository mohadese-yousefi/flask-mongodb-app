from flask import Blueprint


from .blog import urls as blog_urls

blueprint = Blueprint('api/v1', __name__, url_prefix='/api/v1')
blueprint.register_blueprint(blog_urls.blueprint)
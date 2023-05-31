from flask import Blueprint, request, Response
from flask.views import MethodView
from marshmallow.exceptions import ValidationError
from mongoengine.errors import NotUniqueError

from app.app import db, ma, custom_response 
from app.blog.database.models import User, Post, Comment 
from app.blog.database.schemas import PostSchema 


class PostAPI(MethodView):
    def get(self, post_id):
        if post_id is None:
            resp = PostSchema(many=True).dumps(Post.objects)
            return custom_response(200, 'Success', data=resp)

        post = Post.objects.get_or_404(id=post_id)
        resp = PostSchema().dumps(post)
        return custom_response(200, 'Success', data=resp)

    def post(self):
        try:
            #TODO: use session or token
            #user_id = '64731ec35a8aea16197231ef'
            #user = User.objects.get(id=user_id)
            user = User.objects.first()
            data = request.get_json(force=True)

            data = PostSchema().load(data)
            post = Post(**data, owner=user)
            post.save()
            return custom_response(200, 'Success', data=PostSchema().dump(post))
        except ValidationError as e:
            return custom_response(400, e.messages)
        except NotUniqueError:
            return custom_response(400, 'title already exists')
    
    def put(self, post_id):
        try:
            #TODO: check only owner could be edit the post
            post = Post.objects.get_or_404(id=post_id)

            data = request.get_json(force=True)
            data = PostSchema().load(data, partial=True)
            post.update(**data)
            post.save()
            return custom_response(200, 'Success', data=data)
        except ValidationError as e:
            return custom_response(400, e.messages)
        except NotUniqueError:
            return custom_response(400, 'title already exists')
    

    def delete(self, post_id):
        try:
            #TODO: check only owner could be delete the post

            post = Post.objects.get_or_404(id=post_id)
            post.delete()
            return custom_response(200, 'Success') 
        except OperationError as e:
            return custom_response(400, 'Operational error')

post_api = PostAPI.as_view('posts')

blueprint = Blueprint("posts", __name__, url_prefix="/posts")
blueprint.add_url_rule('/', view_func=post_api, methods=['POST'])
blueprint.add_url_rule('/', view_func=post_api, defaults={'post_id': None}, methods=['GET'])
blueprint.add_url_rule('/<string:post_id>', view_func=post_api, methods=['GET', 'PUT', 'DELETE'])
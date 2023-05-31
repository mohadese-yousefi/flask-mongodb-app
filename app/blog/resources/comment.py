from flask import Blueprint, request, Response
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError
from mongoengine.errors import NotUniqueError, DoesNotExist

from app.app import db, ma, custom_response 
from app.blog.database.models import User, Post, Comment 
from app.blog.database.schemas import CommentSchema 


class CommentAPI(MethodView):
    def get(self, post_id, comment_id):
        try:
            post = Post.objects.get(id=post_id)
        except DoesNotExist:
            return custom_response(404, 'Error')

        if comment_id is None:
            resp = CommentSchema(many=True).dumps(comment.objects)
            return custom_response(200, 'Success', data=resp)

        comment = Comment.objects.get_or_404(id=comment_id)
        resp = CommentSchema().dumps(comment)
        return custom_response(200, 'Success', data=resp)

    @jwt_required()
    def post(self, post_id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            post = Post.objects.get_or_404(id=post_id, owner=user)
            data = request.get_json(force=True)

            data = CommentSchema().load(data)
            comment = Comment(**data, sender=user)
            comment.save()
            return custom_response(200, 'Success', data=CommentSchema().dump(comment))
        except ValidationError as e:
            return custom_response(400, e.messages)
    
    @jwt_required()
    def put(self, post_id, comment_id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            post = Post.objects.get_or_404(id=post_id)
            for comment in post.content:
                if str(comment.id) == comment:
                    break
                else:
                    return custom_response(404, 'Error')

            data = request.get_json(force=True)
            data = CommentSchema().load(data, partial=True)
            comment.text = data.get('text') 
            post.update(**data)
            post.save()
            return custom_response(200, 'Success', data=data)

        except ValidationError as e:
            return custom_response(400, e.messages)
    

    @jwt_required()
    def delete(self, post_id, comment_id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            post = Post.objects.get_or_404(id=post_id, user=user)
            for comment in post.content:
                if str(comment.id) == comment:
                    break
                else:
                    return custom_response(404, 'Error')

            post.comment.remove()
            post.save()
            return custom_response(200, 'Success') 
        except OperationError as e:
            return custom_response(400, 'Operational error')


comment_api = CommentAPI.as_view('comments')

blueprint = Blueprint("comments", __name__, url_prefix="/posts")
blueprint.add_url_rule('/<string:post_id>/comments/', view_func=comment_api, methods=['POST'])
blueprint.add_url_rule('/<string:post_id>/comments/', view_func=comment_api, defaults={'post_id': None}, methods=['GET'])
blueprint.add_url_rule('/<string:post_id>/comments/<string:comment_id>', view_func=comment_api, methods=['GET', 'PUT', 'DELETE'])

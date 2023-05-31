from bson import ObjectId
from marshmallow import fields, validate

from app.app import ma


ma.Schema.TYPE_MAPPING[ObjectId] = fields.String


class UserSchema(ma.Schema):
    id = fields.String(dump_only=True)
    email = fields.Email(required=True, validate=validate.Length(max=64))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=64))

    class Meta:
        ordered = True


class CommentSchema(ma.Schema):
    text = fields.String(required=True)
    sender = fields.Nested(UserSchema, dump_only=True)

    class Meta:
        additional = ('id', 'date_created')
        dump_only = ('id', 'date_created')


class PostSchema(ma.Schema):
    title = fields.String(required=True)
    status = fields.String(required=True, validate=validate.OneOf(["active", "archived"]))
    owner = fields.Nested(UserSchema, required=True, dump_only=True)
    comments = fields.Nested(CommentSchema, many=True, dump_only=True)

    class Meta:
        ordered = True
        additional = ('id', 'date_created')
        dump_only = ('id', 'date_created')

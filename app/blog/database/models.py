from datetime import datetime

from app.app import db


class Comment(db.EmbeddedDocument):
    text = db.StringField(required=True)
    date_created = db.DateTimeField(default=datetime.utcnow)
    sender = db.ReferenceField(User)


class Post(db.Document):
    title = db.StringField(required=True, unique=True)
    status = db.StringField(required=True)
    date_created = db.DateTimeField(default=datetime.utcnow)
    comments = db.ListField(db.EmbeddedDocumentField(Comment))
    owner = db.ReferenceField(User)

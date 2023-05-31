from datetime import datetime

from flask_bcrypt import generate_password_hash, check_password_hash

from app.app import db


class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


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

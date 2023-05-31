from datetime import timedelta

from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from marshmallow.exceptions import ValidationError
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist

from app.app import custom_response
from app.users.database.models import User
from app.users.database.schemas import UserSchema


class RegisterAPI(MethodView):
    def post(self):
        try:
            data = request.get_json()

            result = UserSchema().load(data)
            user = User(**result)
            user.hash_password()
            user.save()
            return custom_response(200, 'Success', data=UserSchema().dump(user))

        except ValidationError as e:
            return custom_response(400, e.messages)

        except FieldDoesNotExist:
            return custom_response(400, 'Request is missing required fields')

        except NotUniqueError:
            return custom_response(400, 'Email address already exists')

class LoginAPI(MethodView):
    def post(self):
        try:
            data = request.get_json()
            user = User.objects.get(email=data.get('email'))
            authorized = user.check_password(data.get('password'))
            if not authorized:
                return custom_response(401, 'Email or password invalid')

            expires = timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return custom_response(200, 'Success', data={'token': access_token})

        except DoesNotExist:
            return custom_response(400, 'Email address dose not exists')


registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')

blueprint = Blueprint("auth", __name__, url_prefix="/auth")
blueprint.add_url_rule("/register", view_func=registration_view)
blueprint.add_url_rule("/login", view_func=login_view)
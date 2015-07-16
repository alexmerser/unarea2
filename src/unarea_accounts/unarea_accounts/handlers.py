from datetime import datetime
import json
from flask import request
from flask.ext.restful import marshal
from unarea_core.ext.restfull import ResouceHandler
from unarea_accounts.validators import new_user_validator, login_user_validator
from unarea_accounts.models import USER_MODEL
from unarea_accounts.decorators import is_authorized
from unarea_core.lib.api import CreatedApiResponse


class UserSigninHandler(ResouceHandler):
    def post(self):
        data = request.data
        parsed = new_user_validator.parse(data)
        token = USER_MODEL.get_auth_token(parsed)
        return {'Authorized': {'auth_token': token}}


class UserSignupHandler(ResouceHandler):
    def post(self):
        new_user_spec = new_user_validator.parse(request.data)
        new_user = USER_MODEL.create_user(**new_user_spec)
        token = USER_MODEL.generate_confirmation_token(new_user.email)
        return token, 201


class UserActivationHandler(ResouceHandler):
    def post(self, activation_token):
        email = USER_MODEL.confirm_token(activation_token)
        user = USER_MODEL.get_by(email=email)
        if user.active:
           return "ACTIVE", 400
        else:
            user.active = True
            user.confirmed_at = datetime.now()
            user.save()
            return {'ACTIVATED': user.get_id()}, 200

class UserSignoutHandler(ResouceHandler):
    def post(self):
        pass


class UserHandler(ResouceHandler):
    def get(self):
        pass


class UserProfileHandler(ResouceHandler):
    decorators = [is_authorized]

    def get(self, user_id):
        user = USER_MODEL.get_user(user_id)
        return json.dumps({'user_id': user.email})

    def put(self):
        pass

    def delete(self):
        pass
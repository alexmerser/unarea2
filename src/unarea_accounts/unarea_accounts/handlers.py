import json
from flask import request
from unarea_core.ext.restfull import ResouceHandler
from unarea_accounts.validators import new_user_validator
from unarea_accounts.models import USER_MODEL
from unarea_accounts.decorators import is_authorized


class UserSigninHandler(ResouceHandler):
    def post(self):
        data = request.data
        parsed = new_user_validator.parse(data)
        token = USER_MODEL.get_auth_token(parsed)
        return {'Authorized': {'auth_token': token}}


class UserSignupHandler(ResouceHandler):
    def post(self):
        data = request.data
        parsed = new_user_validator.parse(data)
        new_user = USER_MODEL.create_user(**parsed)
        return json.dumps({'user_id': new_user.get_id()})


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
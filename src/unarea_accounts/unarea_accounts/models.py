import uuid
from datetime import datetime
from datetime import timedelta
from flask_security import MongoEngineUserDatastore
from flask_security.utils import encrypt_password

from unarea_core.db import mongodb
from unarea_core.lib.smart_slugify import slugify
from data_objects import User, Role

class UserModel(MongoEngineUserDatastore):
    def __init__(self):
        super(UserModel, self).__init__(mongodb, User, Role)

    @staticmethod
    def secure_password(password):
        return encrypt_password(password)

    def create_user(self, email, password,
                    active=False, roles=None, username=None,
                    *args, **kwargs):

        username = username or slugify(email.split('@')[0])

        new_user = self.user_model.objects.create(
            username=username,
            email=email,
            password=self.secure_password(password),
            active=active,
            roles=roles)
        return new_user

    def create_role(self, name, description=None):
        return self.role_model.objects.create(
            name=name,
            description=description
        )

    def get_auth_token(self, authorization_data):
        email = authorization_data.get('email', None)
        password = authorization_data.get('password', None)
        remember = authorization_data.get('remember', False)
        user = self.user_model.objects.get(email=email, password=self.secure_password(password))
        user.auth_token = str(uuid.uuid4())
        if remember:
            user.remember = True
            user.token_expired_date = datetime.utcnow() + timedelta(days=30)
        user.save()
        return user.auth_token

    def get_by_token(self, token):
        user = self.user_model.objects(auth_token=str(token))
        return user

USER_MODEL = UserModel()

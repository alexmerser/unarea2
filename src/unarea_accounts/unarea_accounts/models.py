import uuid
from datetime import datetime
from datetime import timedelta
from flask import current_app

from flask_security import MongoEngineUserDatastore
from flask_security.utils import encrypt_password
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from unarea_core.db import mongodb
from unarea_core.lib.smart_slugify import slugify
from data_objects import User, Role, UserAccount

class UserModel(MongoEngineUserDatastore):
    def __init__(self):
        super(UserModel, self).__init__(mongodb, User, Role)

    @staticmethod
    def secure_password(password):
        return encrypt_password(password)

    @staticmethod
    def generate_confirmation_token(email):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(email)

    @staticmethod
    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                max_age=expiration
            )
        except StandardError:
            return False
        return email

    def create_user(self, email, password,
                    active=False, roles=None, username=None,
                    *args, **kwargs):

        username = username or slugify(email.split('@')[0])
        full_name = kwargs.get('full_name')
        birth_day = kwargs.get('birth_day')
        new_user = self.user_model(
            username=username,
            email=email,
            password=generate_password_hash(password),
            active=active,
            roles=roles)
        new_user.save()
        account_info = UserAccount(user_id=new_user.get_id(), full_name=full_name, birth_day=birth_day)
        account_info.save()
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
        user = self.user_model.objects.get(email=email)
        check_password_hash(user.password, password)
        user.auth_token = str(uuid.uuid4())
        if remember:
            user.remember = True
            user.token_expired_date = datetime.utcnow() + timedelta(days=30)
        user.save()
        return user.auth_token

    def get_by_token(self, token):
        user = self.user_model.objects(auth_token=str(token))
        return user

    def get_by(self, **kwargs):
        user = self.user_model.objects(**kwargs)[0]
        return user


USER_MODEL = UserModel()

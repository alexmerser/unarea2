import json
from flask_testing import TestCase

from unarea_core.build import create_app
from unarea_accounts.models import User


class UnareaUserApiSpec(TestCase):
    def create_app(self):
        app = create_app()
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app

    def setUp(self):
        self.app = self.create_app().test_client()

    def tearDown(self):
        User.objects.all().delete()

    def test_user_registration(self):
        User.objects.all().delete()
        resp = self.app.post('/api/v1/accounts/signup', data=json.dumps({
            "email": "email@some.com",
            "password": "pass1234",
            "confirm": "confirm",
            "full_name": "Super Full Name",
            "birth_day": "14.12.2001"}))
        assert resp.status_code, 201

    def test_user_activation(self):
        resp = self.app.post('/api/v1/accounts/signup', data=json.dumps({
            "email": "email@some.com",
            "password": "pass1234",
            "confirm": "confirm",
            "full_name": "Super Full Name",
            "birth_day": "14.12.2001"}))
        assert resp.status_code, 201
        activation_toke = json.loads(resp.data)
        resp = self.app.post('/api/v1/accounts/activate/%s' % activation_toke)
        self.assert200(resp)
        data = json.loads(resp.data)['ACTIVATED']
        saved_user = User.objects.get(id=data)
        self.assertTrue(saved_user.active)
        self.assertIsNotNone(saved_user.confirmed_at)
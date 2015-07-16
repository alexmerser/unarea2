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

    def test_user_signing_up(self):
        User.objects.all().delete()
        resp = self.app.post('/api/v1/accounts/signup', data=json.dumps({
            "email": "email@some.com",
            "password": "pass1234",
            "confirm": "confirm",
            "full_name": "Super Full Name",
            "birth_day": "14.12.2001"}))
        assert resp.status_code, 201

    def test_user_signing_in(self):
        resp = self.app.post('/api/v1/accounts/signup', data=json.dumps({
            "email": "email@some.com",
            "password": "pass1234",
            "confirm": "confirm",
            "full_name": "Super Full Name",
            "birth_day": "14.12.2001"}))
        assert resp.status_code, 201

        resp = self.app.post('/api/v1/accounts/signin', data=json.dumps({
            "email": "email@some.com",
            "password": "pass1234"}))
        assert resp.status_code, 200

    def test_user_activation(self):
        resp = self.app.post('/api/v1/accounts/signup', data=json.dumps({
            "email": "email@some.com",
            "password": "pass1234",
            "confirm": "confirm",
            "full_name": "Super Full Name",
            "birth_day": "14.12.2001"}))
        assert resp.status_code, 201
        created = json.loads(resp.data)

        sign_in_resp = self.app.post('/api/v1/accounts/signin', data=json.dumps({
            "email": "email@some.com",
            "password": "pass1234"}))
        assert sign_in_resp.status_code, 200

        loeaded = json.loads(sign_in_resp.data)
        authorization_token = loeaded.get('auth_token')
        resp = self.app.post('/api/v1/accounts/activation/%s' % created['activation_token'],
                             headers={'Authorization': authorization_token})
        self.assert200(resp)
        user_id = json.loads(resp.data)['activated']
        saved_user = User.objects.get(id=user_id)
        self.assertTrue(saved_user.active)
        self.assertIsNotNone(saved_user.confirmed_at)

    def test_user_resend_activation_key(self):
        sign_up_resp = self.app.post('/api/v1/accounts/signup', data=json.dumps({
            "email": "email@some.com",
            "password": "pass1234",
            "confirm": "confirm",
            "full_name": "Super Full Name",
            "birth_day": "14.12.2001"}))
        assert sign_up_resp.status_code, 201

        sign_in_resp = self.app.post('/api/v1/accounts/signin', data=json.dumps({
            "email": "email@some.com",
            "password": "pass1234"}))
        assert sign_in_resp.status_code, 200

        loeaded = json.loads(sign_in_resp.data)
        authorization_token = loeaded.get('auth_token')
        authorized = User.objects.get(email=loeaded['Authorized'])
        self.assertFalse(authorized.active)

        resp = self.app.post('/api/v1/accounts/activation/resend', headers={'Authorization': authorization_token})
        assert resp.status_code==301, resp.data
        resend_data = json.loads(resp.data)
        confirm = self.app.post(resend_data['confirm_url'], headers={'Authorization': authorization_token})
        self.assert200(confirm)
        saved_user = User.objects.get(id=authorized.get_id())
        self.assertTrue(saved_user.active)
        self.assertIsNotNone(saved_user.confirmed_at)
import json
from flask_testing import TestCase

from unarea_core.build import create_app
from unarea_accounts.models import User

class UnareaUserApiSpec(TestCase):
    def create_app(self):
        return create_app()

    def setUp(self):
        self.app = self.create_app().test_client()

    def tearDown(self):
        pass

    def test_user_registration(self):
        User.objects.all().delete()
        resp = self.app.post('/api/accounts/register', data=json.dumps({'email': 'test@user235s.com',
                                                           'password': 'atata'}))
        self.assert200(resp)
        self.assertIn('user_id', resp.data)
        self.assertIsNotNone(json.loads(resp.data)['user_id'])

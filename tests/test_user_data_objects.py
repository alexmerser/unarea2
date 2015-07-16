# coding: utf-8
from flask_testing import TestCase
from unarea_core.build import create_app
from unarea_accounts.data_objects import User, Role
from unarea_accounts.models import USER_MODEL

class UserModelsSpec(TestCase):

    def create_app(self):
        app = create_app()
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return create_app()

    def setUp(self):
        User.objects.all().delete()
        Role.objects.all().delete()
        self.user_dict = {
            u'email': u'test@user.com',
            u'password': u'test_pass',
        }

        self.role = USER_MODEL.create_role(
            name=u'regular',
            description=u'test role!'
        )
        self.user = USER_MODEL.create_user(**self.user_dict)

    def tearDown(self):
        User.objects.all().delete()
        Role.objects.all().delete()

    def test_user_fields(self):
        self.assertIsInstance(self.user, User)

    # def test_create_user(self):
    #     user = USER_MODEL.create_user(email=u'user.mega-mail.lol@email.com',
    #                                   password=u'super_pass')
    #     self.assertEqual(user.username, u'usermega-maillol')
    #     self.assertEqual(user.email, u'user.mega-mail.lol@email.com')

    def test_role_field(self):
        self.assertEqual(self.role.name, u'regular')
        self.assertEqual(self.role.description, u'test role!')

    def test_create_role(self):
        role = USER_MODEL.create_role(u'test role', description=u'test description')
        self.assertEqual(role.name, u'test role')
        self.assertEqual(role.description, u'test description')

    def test_add_role_to_user(self):
        self.user.roles.append(self.role)
        self.assertEqual(self.user.roles[0], self.role)
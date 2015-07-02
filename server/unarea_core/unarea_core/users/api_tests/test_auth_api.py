import json
import tornado.testing
from flexmock import flexmock

from unarea_core.server.server import Server
from unarea_core.session.models import SessionModel
from unarea_core.users.models import UserModel
from unarea_core.users.auth.urls import auth_mapping
from unarea_core.session.tests.fixtures import SessionFactory
application = Server(auth_mapping)

class BaseApiTest(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return application


class AuthApi(BaseApiTest):
    def test_login_success(self):
        session = SessionFactory.build()
        flexmock(UserModel).should_receive("get").and_return(flexmock(user_id="id"))
        flexmock(SessionModel).should_receive("get_by_user").and_return(session)

        response = self.fetch(
            path='/auth/sign_in',
            method='POST',
            body=json.dumps({'email': 'user@example.com',
                             'pass': 'user_pass'})
        )
        self.assertEqual(response.code, 201)

    def test_forbidden_on_invalid_credentials(self):
        response = self.fetch(
            path='/auth/sign_in',
            method='POST',
            body='{"email": "user@example.com", "password": "u$ser_pass"}'
        )
        self.assertEqual(response.code, 403)


# * AsyncHTTPTestCase
#     - get_app -- returns tornado.web.Application or other HTTPServer callback
#     - fetch -- synchronously fetch a url
#     - get_http_port -- returns the port used by the server
#     - get_url -- returns an absolute url for the given path on the test
# server
#
#
# Python unit testing framework PyUnit
# important concepts:
#   test fixture -- preparation and cleanup actions (working environment for
#       the testing code.
#   test case -- the smallest testable units (set of inputs --> response)
#   test suite -- a collection of test cases, test suites or both
#   test runner -- a component that executes tests and provides the outcome
#       to the user
#
# * TestCase
#       This class implements the interface needed by the testrunner to allow
#       it to drive the test, and methods that the test code can use to check
#       for and report various kinds of failure.
#   - setUp -- preparation
#   - tearDown -- cleanup
#   - runTest -- perform specific testing code
#
#   - assertEqual -- to check for an expected result
#   - assertFalse -- to verify a condition
#   - assertRaises -- to verify that a specific exception gets raised
#
# * TestSuite -- aggregator of tests and test suites
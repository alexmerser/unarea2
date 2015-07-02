import json
from tornado.web import RequestHandler
from unarea_core.server.responces import ForbiddenApiError
from unarea_core.session.bins import SESSION_MODEL
from unarea_core.users.bins import USER_MODEL


class LoginHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    @staticmethod
    def _process_session(user):
        session = SESSION_MODEL.get_by_user(user)

        if not session:
            print "Session for user not found. Creating..."
            session = SESSION_MODEL.create_session_for_user(user)
        return session

    def write_error(self, status_code, **kwargs):
        self.set_header("content_type", "application/json")
        self.finish("%(code)d: message: %(message)s" % {
            "code": status_code,
            "message": self._reason,
        })

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        email = data.get('email', None)
        password = data.get('pass', None)
        user = USER_MODEL.get({'email': email, 'password': password})
        if not user:
            self.send_error(403, reason="Invalid email/password.")

        session = self._process_session(user)
        self.write(json.dumps({'Unarea-Toke': session.token, 'Session': session.serialize()}))
        self.set_status(201, "Authorized")

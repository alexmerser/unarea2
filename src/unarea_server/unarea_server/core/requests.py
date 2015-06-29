from unarea_server.core.framework.server import BaseRequestHandler
from unarea_server.core.mongosession import MONGO_SESSION
from unarea_server.core.permission import PermissionMixIn


class AuthorizedRequestHandler(BaseRequestHandler, PermissionMixIn):
    _session_model = MONGO_SESSION

    def get_current_user(self):
        user_id = self._session['user_id'] if 'user_id' in self._session else None
        return user_id

    def _get_token(self):
        if "Authorization" not in self.request.headers:
            raise self.send_error(403)

        auth = self.request.headers['Authorization']
        if not auth.startswith('UAuthToken='):
            raise self.send_error(403)
        token = auth.partition("=")[2]
        return token

    @property
    def session(self):
        if hasattr(self, '_session'):
            return self._session
        else:
            token = self._get_token()
            session = self._session_model.get_by_token(token)
            if session:
                self._session = session

            return self._session

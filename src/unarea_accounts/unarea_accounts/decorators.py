from functools import wraps
from flask import request
from unarea_accounts.exceptions import UnauthorizedError
from unarea_accounts.models import USER_MODEL



def is_authorized(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if not token:
            raise UnauthorizedError()
        user = USER_MODEL.get_by_token(token=token)
        if user is not None:
            return f(*args, **kwargs)

    return decorated_function

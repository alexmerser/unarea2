from unarea_core.bins import API_HANDLER_FACTORY
from unarea_core.users.auth.handlers import LoginHandler
auth_mapping = [
    (r"/auth/sign_in", LoginHandler),
    (r"/auth/sign_out", API_HANDLER_FACTORY(post=None)),
    (r"/auth/reset_password", API_HANDLER_FACTORY(post=None))
]
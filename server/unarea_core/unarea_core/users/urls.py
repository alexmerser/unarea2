from unarea_core.bins import API_HANDLER_FACTORY
from unarea_core.users.auth.urls import auth_mapping
from unarea_core.users.handlers import GetUserHandler

user_mapping = [
    (r"/user/<user_id>", API_HANDLER_FACTORY(get=GetUserHandler)),
    (r"/user", API_HANDLER_FACTORY(post=None)),
    (r"/users", API_HANDLER_FACTORY(get=None))
]

user_mapping.extend(auth_mapping)

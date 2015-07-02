from unarea_core.server.api import ApiHandlerMeta
from unarea_core.server.responces import OkResponse
from unarea_core.users.bins import USER_MODEL

class GetUserHandler(ApiHandlerMeta):
    def decode(self, arguments, payload):
        return arguments

    def handle(self, request):
        user_id = request
        user = USER_MODEL.get_by_id(user_id)
        return user

    def encode(self, request, result):
        return OkResponse(request.serialize())
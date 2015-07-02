from unarea_core.server.api import ApiHandlerMeta
from unarea_publish.bins import POSTS_MODEL


class PostsListHandler(ApiHandlerMeta):
    def decode(self, arguments, payload):
        pass

    def handle(self, request):
        result = u"POSTS"
        return result

    def encode(self, request, result):
        return self.send_response(200, {u"status": result})


class CreatePostHandler(ApiHandlerMeta):
    def decode(self, arguments, payload):
        pass

    def handle(self, request):
        args, body = request
        result = POSTS_MODEL.create_post(body)
        return result

    def encode(self, request, result):
        return self.send_response(200, {u"status": result})


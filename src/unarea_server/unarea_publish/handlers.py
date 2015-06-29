from unarea_server.core.framework.server import BaseHandler
from unarea_publish.entry import POSTS_MODEL

class PostsListHandler(BaseHandler):
    def validate(self, arguments, body):
        return arguments

    def handle(self, request):
        result = u"POSTS"
        return result

    def encode(self, request, result):
        return self.send_response(200, {u"status": result})


class CreatePostHandler(BaseHandler):
    def validate(self, arguments, body):
        return arguments, body

    def handle(self, request):
        args, body = request
        result = POSTS_MODEL.create_post(body)
        return result

    def encode(self, request, result):
        return self.send_response(200, {u"status": result})


from unarea_server.core.framework.server import RequestHandler

from unarea_publish.handlers import PostsListHandler

posts_mapping = [
    (r"/posts", RequestHandler(get_handler=PostsListHandler))
]

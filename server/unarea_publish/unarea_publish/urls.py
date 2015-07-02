from unarea_core.bins import API_HANDLER_FACTORY

from unarea_publish.handlers import PostsListHandler

posts_mapping = [
    (r"/posts", API_HANDLER_FACTORY(get=PostsListHandler))
]

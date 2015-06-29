from unarea_server.core.framework.server import RequestHandler

from unarea_base.handlers import MainHandler, AboutHandler

default_mapping = [
    (r'/$', RequestHandler(get_handler=MainHandler)),
    (r'/about$', RequestHandler(get_handler=AboutHandler)),
]

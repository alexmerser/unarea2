from unarea_server.core.framework.server import Server
from unarea_server.entry import URLS_MAP
from unarea_messages.app import app

server = Server(URLS_MAP)


server.register_container(app)

def runserver():
    print server.handlers
    server.start_as_wsgi(port=8000)

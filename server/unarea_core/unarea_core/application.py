import logging
from optparse import OptionParser

from unarea_core.server.server import Server
from users.urls import user_mapping

log = logging.getLogger("unarea_core." + __name__)

core_server = Server(user_mapping)

def init_from_cmd_params():
    parser = OptionParser(usage="usage: %prog [options] port")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("You should provide port number")
    port = None
    try:
        port = int(args[0])
    except (ValueError, TypeError):
        parser.error("Port should be numeric")

    return {'port': port}


def start_server(port, prefork=True):
    log.info("start_server(): starting")

    core_server.start(port, prefork)

def main():
    params = init_from_cmd_params()

    start_server(params['port'])
# coding=utf-8
import wsgiref.simple_server
import tornado.httpserver
from tornado.web import FallbackHandler
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.wsgi import WSGIContainer


class Server(Application):
    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)

    @property
    def as_wsgi(self):
        """
        Adapt server to a WSGI application for deploy, for example, on GoogleAppEngine.

        WARNING! Due to Tornado specification in WSGI mode asynchronous methods are not supported.
        Is not possible to use AsyncHTTPClient, or the tornado.auth or tornado.websocket modules.

        :return: application instance as WSGI application
        :rtype: tornado.wsgi.WSGIAdapter
        """
        return tornado.wsgi.WSGIAdapter(self)

    def register_container(self, container, host_pattern=None):
        """
        Register WSGI application as server app and use main application server as proxy.

        WARNING! Reade it, because DisperengServer based on Tornado Application instance.

        WSGI is a synchronous interface, while Tornado’s concurrency model is based on single-threaded
        asynchronous execution. This means that running a WSGI app with Tornado’s WSGIContainer is less
        scalable than running the same app in a multi-threaded WSGI server like gunicorn or uwsgi.
        Use WSGIContainer only when there are benefits to combining Tornado and WSGI
        in the same process that outweigh the reduced scalability.

        :param container: wsgi application. For example Flask application instance
        :type container: WSGIApplication

        :param host_pattern: host pattern for container
        :type host_pattern: str
        """
        self.add_handlers(
            host_pattern=r"%s" % host_pattern or self.default_host,
            host_handlers=[
                (r".*", FallbackHandler, dict(fallback=WSGIContainer(container)))
            ]
        )

    def start(self, port=8000, prefork=True, num_processes=1):
        """
        Start serving server application instance

        :param port: listen port
        :type port: int

        :param prefork: flag that indicate if this application is running in multiprocess
        :type prefork: bool

        :param num_processes: number of processes
        :type num_processes: int
        """
        http_server = tornado.httpserver.HTTPServer(self)
        if prefork:
            http_server.bind(port)
            http_server.start(num_processes)
        else:
            http_server.listen(port)
        IOLoop.instance().start()

    def start_as_wsgi(self, host='localhost', port=8000):
        """
        Start application as WSGI application

        :param host: application host. Default `localhost:8000`
        :type host: str

        :param port: application port
        :type port: int
        """
        server = wsgiref.simple_server.make_server(host, port, self.as_wsgi)
        server.serve_forever()
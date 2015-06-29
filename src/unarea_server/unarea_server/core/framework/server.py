# coding=utf-8
import json
from logging import getLogger
import wsgiref.simple_server
from abc import abstractmethod

import tornado.httpserver
from tornado.web import FallbackHandler
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.web import RequestHandler as TornadoRequestHandler
from tornado.wsgi import WSGIContainer

__all__ = ["Server"]

log = getLogger('unarea_server.' + __name__)


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


class BaseResponse(object):
    def __init__(self, code, result=None, content_type="application/json", cookie=None, headers=None):
        self.code = code
        self.result = json.dumps(result)
        self.content_type = content_type
        self.cookie = cookie if cookie else {}
        self.headers = headers if headers else {}


class BaseHandler(object):

    response = None

    @classmethod
    def send_response(cls, code, result, **kwargs):
        """

        :param code:
        :param result:
        :param kwargs:
        :return:
        """
        if cls.response:
            return cls.response(code, result, **kwargs)
        return BaseResponse(code, result)

    @abstractmethod
    def validate(self, arguments, body):
        """

        :param arguments:
        :param body:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def handle(self, request):
        """

        :param request:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def encode(self, request, result):
        """

        :param request:
        :param result:
        :return:
        """
        raise NotImplementedError


class RequestContext(object):
    def __init__(self, session, user):
        """

        :param session: session document for request
        :type session: UserSession object

        :param user: user document for request
        :type user: User
        """
        self.session = session
        self.user = user

class BaseRequestHandler(TornadoRequestHandler):

    def data_received(self, chunk):
        pass

    @staticmethod
    def _run_handler(handler, arguments, body):
        """

        :param handler:
        :param arguments:
        :param body:
        :return:
        """
        decoded_request = handler.validate(arguments, body)
        result = handler.handle(decoded_request)
        return handler.encode(decoded_request, result)

    def _dispatch_request(self, handler, arguments, body):
        """

        :param handler:
        :param arguments:
        :param body:
        :return:
        """
        return self._run_handler(handler, arguments, body)

    def _decode_request(self, url_args):
        """
        :param url_args:
        :return:
        """
        arguments = {key.decode('utf-8'): value[0].decode('utf-8') for key, value in
                     self.request.arguments.iteritems()}
        request_body = self.request.body.decode('utf-8')
        if self.request.headers.get("content-type", "").partition(";")[0].strip() == "application/json":
            json_arguments = json.loads(request_body) if request_body != "" else {}
            arguments.update(json_arguments)
        url_args = dict(zip(url_arguments or [], url_args))
        arguments.update(url_args)
        return arguments, request_body

    def process_request(self, handler, *args, **kwargs):
        """

        :param handler:
        :param args:
        :param kwargs:
        :return:
        """
        assert handler is None or issubclass(handler, BaseHandler)
        arguments, body = self._decode_request(args)

        request_handler = handler()
        handled_result = self._dispatch_request(request_handler, arguments, body)
        self.write(handled_result.result)
        self.set_header("DISPERENG_CUSTOM", "custom_header")
        self.set_header("Content-Type", handled_result.content_type)
        self.set_header("Cache-Control", "private, must-revalidate")
        for name, value in handled_result.cookie.items():
            self.set_cookie(name, value)
        for header, value in handled_result.headers.iteritems():
            self.set_header(header, value)

class SessionRequestHandler(BaseRequestHandler, PermissionMixIn, FlashMessageMixIn, CachedItemsMixIn):

    def get_current_user(self):
        user = self.session['user'] if 'user' in self.session else None
        return user

    @property
    def session(self):
        if hasattr(self, '_session'):
            return self._session
        else:
            self.require_setting('permanent_session_lifetime', 'session')
            expires = self.settings['permanent_session_lifetime'] or None
            if 'redis_server' in self.settings and self.settings['redis_server']:
                sessionid = self.get_secure_cookie('sid')
                self._session = RedisSession(self.application.session_store, sessionid, expires_days=expires)
                if not sessionid:
                    self.set_secure_cookie('sid', self._session.id, expires_days=expires)
            else:
                self._session = Session(self.get_secure_cookie, self.set_secure_cookie, expires_days=expires)
            return self._session

    def get_user_locale(self):
        code = self.get_cookie('lang', self.settings.get('default_locale', 'zh_CN'))
        return tornado.locale.get(code)

    def get_template_path(self):
        if 'theme_template_path' in self.settings:
            return self.settings['theme_template_path']
        return self.settings.get('template_path')

    def get_error_html(self, status_code, **kwargs):
        if self.settings.get('debug', False) is False:
            self.set_status(status_code)
            return self.render_string('errors/%s.html' % status_code)

        else:
            def get_snippet(fp, target_line, num_lines):
                if fp.endswith('.html'):
                    fp = os.path.join(self.get_template_path(), fp)

                half_lines = (num_lines/2)
                try:
                    with open(fp) as f:
                        all_lines = [line for line in f]
                        code = ''.join(all_lines[target_line-half_lines-1:target_line+half_lines])
                        formatter = HtmlFormatter(linenos=True, linenostart=target_line-half_lines, hl_lines=[half_lines+1])
                        lexer = get_lexer_for_filename(fp)
                        return highlight(code, lexer, formatter)

                except Exception, ex:
                    logging.error(ex)
                    return ''

            css = HtmlFormatter().get_style_defs('.highlight')
            exception = kwargs.get('exception', None)
            return self.render_string('errors/exception.htm',
                                      get_snippet=get_snippet,
                                      css=css,
                                      exception=exception,
                                      status_code=status_code,
                                      kwargs=kwargs)

    def get_args(self, key, default=None, type=None):
        if type==list:
            if default is None: default = []
            return self.get_arguments(key, default)
        value = self.get_argument(key, default)
        if value and type:
            try:
                value = type(value)
            except ValueError:
                value = default
        return value

    @property
    def forms(self):
        return self.application.forms[self.locale.code]

    def _(self, message, plural_message=None, count=None):
        return self.locale.translate(message, plural_message, count)

def RequestHandler(url_arguments=None, get_handler=None, post_handler=None, put_handler=None,
                    delete_handler=None, update_handler=None):
    """
    Request factory method (may be temporary before factory class)

    :param url_arguments: url arguments to parse
    :type url_arguments: list

    :param get_handler: GET request handler
    :type get_handler: BaseHandler

    :param post_handler: POST
    :type post_handler: BaseHandler

    :param put_handler: PUT
    :type put_handler: BaseHandler

    :param delete_handler: DELETE
    :type delete_handler: BaseHandler

    :param update_handler: PATCH
    :type update_handler: BaseHandler

    :return: request handler
    :rtype: RequestHandler
    """

    class _RequestHandler(TornadoRequestHandler):

        def data_received(self, chunk):
            pass

        @staticmethod
        def _run_handler(handler, arguments, body):
            """

            :param handler:
            :param arguments:
            :param body:
            :return:
            """
            decoded_request = handler.validate(arguments, body)
            result = handler.handle(decoded_request)
            return handler.encode(decoded_request, result)

        def _dispatch_request(self, handler, arguments, body):
            """

            :param handler:
            :param arguments:
            :param body:
            :return:
            """
            return self._run_handler(handler, arguments, body)

        def _decode_request(self, url_args):
            """
            :param url_args:
            :return:
            """
            arguments = {key.decode('utf-8'): value[0].decode('utf-8') for key, value in
                         self.request.arguments.iteritems()}
            request_body = self.request.body.decode('utf-8')
            if self.request.headers.get("content-type", "").partition(";")[0].strip() == "application/json":
                json_arguments = json.loads(request_body) if request_body != "" else {}
                arguments.update(json_arguments)
            url_args = dict(zip(url_arguments or [], url_args))
            arguments.update(url_args)
            return arguments, request_body

        def process_request(self, handler, *args, **kwargs):
            """

            :param handler:
            :param args:
            :param kwargs:
            :return:
            """
            assert handler is None or issubclass(handler, BaseHandler)
            arguments, body = self._decode_request(args)

            request_handler = handler()
            handled_result = self._dispatch_request(request_handler, arguments, body)
            self.write(handled_result.result)
            self.set_header("DISPERENG_CUSTOM", "custom_header")
            self.set_header("Content-Type", handled_result.content_type)
            self.set_header("Cache-Control", "private, must-revalidate")
            for name, value in handled_result.cookie.items():
                self.set_cookie(name, value)
            for header, value in handled_result.headers.iteritems():
                self.set_header(header, value)

        def get(self, *args, **kwargs):
            return self.process_request(get_handler, *args, **kwargs)

        def post(self, *args, **kwargs):
            return self.process_request(post_handler, *args, **kwargs)

        def put(self, *args, **kwargs):
            return self.process_request(put_handler, *args, **kwargs)

        def delete(self, *args, **kwargs):
            return self.process_request(delete_handler, *args, **kwargs)

        def patch(self, *args, **kwargs):
            return self.process_request(update_handler, *args, **kwargs)

    return _RequestHandler
import json
from abc import abstractmethod, ABCMeta
from tornado.web import RequestHandler

from unarea_core.server.base import ApiHandlerMeta, BaseRequestContext
from unarea_core.server.responces import ApiResponseMeta, ApiError, HandlerNotFoundApiError, UnexpectedApiError, \
    ValidationApiError,  ForbiddenApiError, NotFoundApiError, ResponseMeta


class ApiRequestContext(BaseRequestContext):
    def __init__(self, session, user, is_public_api, request_uri):
        """

        :param session: session document for request
        :type session: NimbleSessionDocument

        :param user: user document for request
        :type user: UserDocument

        :param request_uri: requested uri
        :type request_uri: unicode
        """
        self.session = session
        self.user = user
        self.is_public_api = is_public_api
        super(ApiRequestContext, self).__init__(user.user_id, request_uri)

def RequestHandlerMeta(url_args=None, get=None, post=None, put=None, delete=None):

    class _RequestHandler(RequestHandler):
        __metaclass__ = ABCMeta

        @abstractmethod
        def _get_token(self):
            """
            This abstract method must use technology-specific way to extract session token from request
            :return: session token id
            :rtype: str
            """
            raise NotImplementedError

        @abstractmethod
        def _get_context(self, token):
            """
            Each subclass must define it's own implementation of this method. Returned object must be subclass of
            RequestContext class
            :param token:
            :return: request context object
            :rtype: RequestContext
            """
            raise NotImplementedError

        @staticmethod
        def _handle_request(api_handler, arguments, payload):
            arguments = api_handler.validate_arguments(arguments, payload) or arguments
            decoded_request = api_handler.decode(arguments, payload)
            result = api_handler.handle(decoded_request)
            return api_handler.encode(decoded_request, result)

        # def _log_unexpected_error(self, error, context, err_id=None):
        #     copied_context = context.__dict__.copy() if context else None
        #     if copied_context is not None:
        #         copied_context.pop('user', None)
        #     user_id = getattr(context, "user_id", "unknown")
        #     log.critical("Error handling request for user_id <%s>" % user_id, trace=1,
        #                  jsonData={"user_id": str(user_id), "error_id": err_id},
        #                  repr={'exc': error, 'context': copied_context, 'request': self.request.__dict__})

        def _handle_context(self, api_handler, arguments, payload):
            assert api_handler is None or issubclass(api_handler, ApiHandlerMeta)
            if api_handler is not None:
                context = None
                try:
                    context = self._get_context(self._get_token())
                    handler = api_handler(context)
                    result = self._handle_request(handler, arguments, payload)
                    assert isinstance(result, ResponseMeta)
                    return result
                except ApiError:
                    raise
                except Exception as exc:
                    raise exc
                    # err_id = "".join([choice(hexdigits) for _ in xrange(32)])
                    # self._log_unexpected_error(exc, context, err_id)
                    # raise UnexpectedApiError(exc, err_id), None, sys.exc_info()[2]
            else:
                raise HandlerNotFoundApiError()

        def _decode_request(self, urlargs):
            try:
                arguments = {key.decode('utf-8'): value[0].decode('utf-8')
                             for key, value in self.request.arguments.iteritems()}
            except UnicodeDecodeError:
                raise
                # raise ValidationApiError([results.ValidationProblem("query", "Non-UTF8 query arguments")])

            try:
                payload = self.request.body.decode("utf-8")
            except UnicodeDecodeError:
                raise
                # raise ValidationApiError([results.ValidationProblem("query", "Non-UTF8 body")])

            if self.request.headers.get("content-type", "").partition(";")[0].strip() == "application/json":
                try:
                    json_arguments = json.loads(payload) if payload != "" else {}
                except StandardError:
                    raise
                    # raise ValidationApiError([results.ValidationProblem("body", "Malformed JSON body")])
                arguments.update(json_arguments)
            urlargs = dict(zip(url_args or [], urlargs))
            arguments.update(urlargs)
            return arguments, payload

        def _report_error(self, http_error):
            """

            :param http_error:
            :type http_error: HttpApiError
            :return: None
            """
            try:
                self.set_status(http_error.code)
                self.write(http_error.encode() or "")
                self.set_header("Content-Type", "application/json")
            except Exception as exc:
                print exc
                self.set_status(500)
                # self._log_unexpected_error(exc, context=None)

        def dispatch_request(self, apihandler, *args, **kwargs):
            try:
                arguments, payload = self._decode_request(args)
                cb = arguments.pop("callback", None)
                # TODO!!!
                # result = translate_response_to_http(self._handle_context(apihandler, arguments, payload))
                result = self._handle_context(apihandler, arguments, payload)
                self.set_status(result.code)
                if cb is not None:
                    res = "%s(%s)" % (cb, result.result)
                else:
                    res = result.result
                self.write(res)
                self.set_header("Content-Type", result.content_type)
                self.set_header("Cache-Control", "private, must-revalidate")

                for name, value in result.cookie.items():
                    self.set_cookie(name, value)
                for header, value in result.headers.iteritems():
                    self.set_header(header, value)

            except ApiError as error:
                print error
                # TODO:
                # self._report_error(translate_error_to_http(error))
            except Exception as exc:
                print exc
                # self._log_unexpected_error(exc, context=None)
                # self._report_error(HttpUnexpectedApiError(exc))

        def get(self, *args, **kwargs):
            return self.dispatch_request(get, *args, **kwargs)

        def post(self, *args, **kwargs):
            return self.dispatch_request(post, *args, **kwargs)

        def put(self, *args, **kwargs):
            return self.dispatch_request(put, *args, **kwargs)

        def delete(self, *args, **kwargs):
            return self.dispatch_request(delete, *args, **kwargs)

    return _RequestHandler


class ApiHandlerFactory(object):

    def __init__(self, session_model):
        self._session_model = session_model

    def __call__(self, arg_names=None, get=None, post=None, put=None, delete=None):
        handler_meta = RequestHandlerMeta(arg_names, get, post, put, delete)
        session_model = self._session_model

        class _SessionApiHandler(handler_meta):

            def _get_token(self):
                auth_token = None
                if 'Unarea-Token' in self.request.headers:
                    auth_token = unicode(self.request.headers['Unarea-Token'])
                elif 'api_token' in self.request.arguments and len(self.request.arguments['api_token']) == 1:
                    auth_token = unicode(self.request.arguments['api_token'])
                if auth_token is None:
                    return None
                return auth_token

            @staticmethod
            def _load_session(token):
                session = session_model.get_by_token(token)
                if session and session_model.is_valid(session):
                    return session

            @staticmethod
            def get_current_user(session):
                user = session_model.get_user_for_session(session)
                return user

            def _get_context(self, token):
                session = self._load_session(token)

                user = self.get_current_user(session)
                is_public = session.is_api_token
                return ApiRequestContext(session, user, is_public, self.request.uri)

        return _SessionApiHandler
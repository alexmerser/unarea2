import json
from abc import ABCMeta
from bson import ObjectId


class ApiError(StandardError):
    pass

class HandlerNotFoundApiError(ApiError):
    def __init__(self):
        super(HandlerNotFoundApiError, self).__init__()


class UnexpectedApiError(ApiError):
    def __init__(self, reason, err_id=None):
        self.reason = reason
        self.err_id = err_id
        super(UnexpectedApiError, self).__init__()


class ValidationApiError(ApiError):
    def __init__(self, problems):
        self.problems = problems
        super(ValidationApiError, self).__init__()


class ForbiddenApiError(ApiError):
    def __init__(self, message):
        self.message = message
        super(ForbiddenApiError, self).__init__()


class NotAcceptableApiError(ApiError):
    def __init__(self, message):
        self.message = message
        super(NotAcceptableApiError, self).__init__()


class NotFoundApiError(ApiError):
    def __init__(self, object_type, object_id):
        self.object_type = object_type
        self.object_id = object_id
        super(NotFoundApiError, self).__init__()



class ApiResponseMeta(object):
    __metaclass__ = ABCMeta

    def __init__(self, result=None, content_type="application/json", cookie=None):
        if isinstance(result, dict):
            result = json.dumps(result, cls=JSONEncoder)
        self.result = result
        self.content_type = content_type
        self.cookie = cookie if cookie is not None else {}

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super(JSONEncoder, self).default(o)


class SuccessApiResponse(ApiResponseMeta):
    pass


class CreatedApiResponse(ApiResponseMeta):
    pass


class DeletedApiResponse(ApiResponseMeta):
    pass


class UpdatedApiResponse(ApiResponseMeta):
    pass


class ContinueApiResponse(ApiResponseMeta):
    def __init__(self, destination, content_type):
        super(ContinueApiResponse, self).__init__(result=destination, content_type=content_type)


class ResponseMeta(object):
    __metaclass__ = ABCMeta
    code = None

    def __init__(self, result=None, content_type="application/json", cookie=None, headers=None):
        if isinstance(result, dict):
            result = json.dumps(result, cls=JSONEncoder)
        self.result = result
        self.content_type = content_type
        self.headers = headers if headers is not None else {}
        self.cookie = cookie if cookie is not None else {}

class OkResponse(ResponseMeta):
    code = 200


class CreatedResponse(ResponseMeta):
    code = 201


class DeletedResponse(ResponseMeta):
    code = 200


class UpdatedResponse(ResponseMeta):
    code = 200


class ContinueResponse(ResponseMeta):
    code = 303
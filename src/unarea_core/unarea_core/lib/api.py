import json
from bson.objectid import ObjectId

from flask_restful import abort, marshal


class APIJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super(APIJsonEncoder, self).default(o)


class APIResponse(object):
    status_code = None

    def __new__(cls, result, fields=None, headers=None, message=u'', *args, **kwargs):
        if fields:
            encoded_results = marshal(result, fields)
        else:
            encoded_results = result
            encoded_results.update({u'message': message})

        return encoded_results, cls.status_code, headers or {}

class SuccessApiResponse(APIResponse):
    status_code = 200

class CreatedApiResponse(APIResponse):
    status_code = 201

class UpdatedApiResponse(APIResponse):
    status_code = 201

class DeletedApiResponse(APIResponse):
    status_code = 201

class ApiErrorResponse(object):
    status_code = None

    def __init__(self, message, **kwargs):
        self.__call__(message=message, **kwargs)

    @classmethod
    def __call__(cls, **kwargs):
        return abort(cls.status_code, **kwargs)

class NotFoundResponse(ApiErrorResponse):
    status_code = 404

class ForbiddenResponse(ApiErrorResponse):
    status_code = 403


class ServerErrorResponse(ApiErrorResponse):
    status_code = 500

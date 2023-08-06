import json

from flask import request
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = "sorry, we make a mistake"
    api_code = 999

    def __init__(self, msg=None, code=None, api_code=None, headers=None):
        self.code = code or self.code
        self.msg = msg or self.msg
        self.api_code = api_code or self.api_code
        super().__init__(msg, None)

    def get_body(self, envrion=None):
        body = {
            "msg": self.msg,
            "code": self.api_code,
            # POST /v1/client
            "api": f"{request.method} {self.get_url_path()}",
        }
        return json.dumps(body)

    def get_headers(self, environ=None, scope=None):
        return [("Content-Type", "application/json")]

    @staticmethod
    def get_url_path():
        url = str(request.full_path)
        return url.split("?")[0]


class BadRequest(APIException):
    code = 400
    msg = "invalid parameter"
    api_code = 1000


class Unauthorized(APIException):
    code = 401
    msg = "鉴权验证失败"
    api_code = 1100


class Forbidden(APIException):
    code = 403
    msg = "not permisson"
    api_code = 1300


class NotFound(APIException):
    code = 404
    msg = "the resouce is no found"
    api_code = 1400


class ServerError(APIException):
    code = 500
    msg = "server erorr"
    api_code = 2000

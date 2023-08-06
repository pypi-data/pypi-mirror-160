from csv import excel
from functools import wraps
import json
from typing import Any, Callable

from flask import jsonify, request

from flask_fuzhu.exception import BadRequest
from flask_fuzhu.exception import Unauthorized


def need_token(verify_func: Callable[[str], bool] = lambda x: True, token_key: str = "TOKEN"):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get(token_key, None)
            if token is None:
                raise BadRequest(f"Header未包含{token_key}")
            if not verify_func(token):
                raise Unauthorized()
            return func(*args, *kwargs)

        return wrapper

    return inner


def need_args(args_list: list[str]):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            miss_args = [a for a in args_list if request.args.get(a, None) is None]
            if len(miss_args):
                raise BadRequest(f"Url缺少参数:{','.join(miss_args)}")
            return func(*args, *kwargs)

        return wrapper

    return inner


def need_json_key(json_key: dict[str, Any]):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            miss_key = [k for k in json_key if request.get_json().get(k, None) is None]
            if len(miss_key):
                raise BadRequest(f"Body中缺少字段:{','.join(miss_key)}")
            return func(*args, *kwargs)

        return wrapper

    return inner


def return_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if type(ret) == tuple:
            data, status_code = ret
            return jsonify({"code": 1, "data": data}), status_code
        return jsonify({"code": 1, "data": ret}), 200

    return wrapper

from functools import wraps

from flask import request

from flask_fuzhu.exception import BadRequest
from flask_fuzhu.exception import Unauthorized


def need_token(verify_func=lambda x: True, token_key="TOKEN"):
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


def need_args(args_list):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            miss_args = [a for a in args_list if request.args.get(a, None) is None]
            if len(miss_args):
                raise BadRequest(f"Url参数缺少{','.join(miss_args)}")
            return func(*args, *kwargs)

        return wrapper

    return inner

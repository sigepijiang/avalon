# -*- coding: utf-8 -*-
from functools import wraps

from bottle import request


def sigin_required(func):
    @wraps(func)
    def caller(*args, **kwargs):
        if not request.ukey:
            raise

        return func(*args, **kwargs)

    return caller

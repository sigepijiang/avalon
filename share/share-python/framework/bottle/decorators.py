# -*- coding: utf-8 -*-
from functools import wraps

from bottle import request, redirect, url


def signin_required(func):
    @wraps(func)
    def caller(*args, **kwargs):
        if not request.ukey:
            return redirect(url('zeus:account.login', success=request.url))

        return func(*args, **kwargs)

    return caller

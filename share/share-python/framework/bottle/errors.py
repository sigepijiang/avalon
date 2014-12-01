# -*- coding: utf-8 -*-
from bottle import HTTPError, error
from .template import render_template


class NotFound(HTTPError):
    def __init__(self, body):
        super(NotFound, self).__init__(404, body)


class BadRequest(HTTPError):
    def __init__(self, body):
        super(BadRequest, self).__init__(400, body)


class APIUnauthorized(HTTPError):
    def __init__(self, body):
        super(APIUnauthorized, self).__init__(401, body)


class APINotFound(HTTPError):
    def __init__(self, body):
        super(HTTPError, self).__init__(404, body)


class APIBadRequest(HTTPError):
    def __init__(self, body):
        super(HTTPError, self).__init__(400, body)


@error(404)
def error404(error):
    return render_template('http404.html', error=error)


@error(400)
def error400(error):
    return render_template('http400.html', error=error)

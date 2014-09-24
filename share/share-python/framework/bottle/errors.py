# -*- coding: utf-8 -*-
from bottle import HTTPError


class NotFound(HTTPError):
    def __init__(self, body):
        super(NotFound, self).__init__(404, body)


class BadRequest(HTTPError):
    def __init__(self, body):
        super(BadRequest, self).__init__(400, body)


class Unauthorized(HTTPError):
    def __init__(self, body):
        super(Unauthorized, self).__init__(401, body)


class APINotFound(HTTPError):
    def __init__(self, body):
        super(HTTPError, body).__init__(404, body)


class APIBadRequest(HTTPError):
    def __init__(self, body):
        super(HTTPError, body).__init__(400, body)

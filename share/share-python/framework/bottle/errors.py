# -*- coding: utf-8 -*-
from bottle import HTTPError


class NotFound(HTTPError):
    def __init__(self, body):
        super(NotFound, self).__init__(404, body)


class BadRequet(HTTPError):
    def __init__(self, body):
        super(BadRequet, self).__init__(400, body)

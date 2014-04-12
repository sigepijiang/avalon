#-*- coding: utf-8 -*-

from bottle import default_app

from share.restful.client import BaseClient


class Client(BaseClient):
    @property
    def _access_token(self):
        return default_app().access_token

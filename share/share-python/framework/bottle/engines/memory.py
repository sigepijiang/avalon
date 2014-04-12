#-*- coding: utf-8 -*-
from bottle import cached_property
from bottle import default_app

from share.engines.memory import Client


class MemoryManager(object):
    @cached_property
    def memcached(self):
        app = default_app()
        return Client(app.config.memcached)


memory = MemoryManager()

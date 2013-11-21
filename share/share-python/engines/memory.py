#-*- coding: utf-8 -*-
from memcache import Client

from share import app_stack
from bottle import cached_property


class MemoryManager(object):
    @cached_property
    def memcached(self):
        app = app_stack()
        return Client(app.config.memcached)


memory = MemoryManager()

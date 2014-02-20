# -*- coding: utf-8 -*-
import time

from bottle import request

from .errors import APINotFound


METHOD_MAP = {
    'get': 'get',
    'post': 'create',
    'put': 'update',
    'delete': 'delete',
}


def make_path(path):
    return path + '.<format>'


class RESTfulAPI(object):
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    path = ''

    # TODO: resource_id

    @classmethod
    def attach_to(cls, blueprint):
        def view_func(*args, **kwargs):
            view = view_func.view_class()
            return view.dispatch_request(*args, **kwargs)

        view_func.view_class = cls
        view_func.__name__ = 'api_' + cls.__name__.lower()
        view_func.__doc__ = cls.__doc__
        view_func.__module__ = cls.__module__
        view_func.methods = cls.methods

        blueprint.add_url_rule(
            make_path(cls.path), view_func, cls.methods,
            view_func.__name__,
        )
        return view_func

    def dispatch_request(self, *args, **kwargs):
        result_format = kwargs.pop('format', 'json')
        meth = getattr(self, METHOD_MAP[request.method.lower()], None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        if not meth:
            raise APINotFound()

        if result_format == 'json':
            return dict(
                ok=True, time=time.time(), result=meth(*args, **kwargs))

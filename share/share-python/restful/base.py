# -*- coding: utf-8 -*-
import time
from bottle import request

from share.errors import APINotFound

METHOD_MAP = {
    'get': 'get',
    'post': 'create',
    'put': 'update',
    'delete': 'delete',
}


def make_path(path):
    return path + '.<format>'


class RESTfulBaseAPI(object):
    methods = []
    path = ''
    hooks = {}

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

    def implement(self):
        raise NotImplementedError()

    # TODO: 改进参数
    def authorize(self):
        raise NotImplementedError()

    # TODO: 改进参数
    def before_request(self, meth):
        raise NotImplementedError()

    # TODO: 改进参数
    def after_request(self, meth):
        raise NotImplementedError()

    def dispatch_request(self, *args, **kwargs):
        self.implement()
        result_format = kwargs.pop('format', 'json')
        meth = getattr(self, METHOD_MAP[request.method.lower()], None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        if not meth:
            raise APINotFound()

        if getattr(meth, 'authorization_required', False):
            self.authorize()

        result = None
        if result_format == 'json':
            result = dict(
                ok=True, time=time.time(), result=meth(*args, **kwargs))
        self.after_request(meth)
        return result

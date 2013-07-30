# -*- coding: utf-8 -*-
import os
import codecs
import markdown2
from bottle import request

from .errors import NotFound
from .template import get_template_path


CONTENT_CONVERTER = {
    'md': markdown2.markdown,
    'org': '',
}


def content2html(func):
    def call_f(*args, **kwargs):
        result = func(*args, **kwargs)

        # 固定寻找<app>/templates/(md|org)/下的文件
        template_path = get_template_path()[0]
        file_name = result.pop('file_name')
        file_type = result.pop('file_type')

        full_path = os.path.join(template_path, file_name + '.' + file_type)
        if os.path.exists(full_path):
            raise NotFound('页面不存在')

        with codecs.open(full_path, 'r', 'utf-8') as f:
            content = f.read()
        content = CONTENT_CONVERTER[file_type](content)
        result['content'] = content
        return result
    return call_f


HTTP_METHOD_MAP = {
    'get': 'get',
    'push': 'create',
    'put': 'update',
    'delete': 'delete'
}


class MethodView(object):
    decorators = []
    methods = []

    def __init__(self, *args, **kwargs):
        super(MethodView, self).__init__()

    @classmethod
    def as_view(cls, name=''):
        def view_func(*args, **kwargs):
            self = view_func.view_class(*args, **kwargs)
            return self.dispatch_request(*args, **kwargs)

        if cls.decorators:
            view_func.__name__ = name
            view_func.__module__ = cls.__module__
            for decorator in cls.decorators:
                view_func = decorator(view_func)

        view_func.view_class = cls
        view_func.__name__ = name
        view_func.__doc__ = cls.__doc__
        view_func.__module__ = cls.__module__
        view_func.methods = cls.methods
        return view_func

    def dispatch_request(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        if not meth:
            raise
        return meth(*args, **kwargs)

# -*- coding: utf-8 -*-
import os
import functools

from bottle import Bottle
from bottle import Route
from bottle import RouteBuildError
from bottle import makelist
from bottle import request
from bottle import template


HTTP_METHOD_MAP = {
    'get': 'get',
    'push': 'create',
    'put': 'update',
    'delete': 'delete'
}


class Avalon(Bottle):
    def __init__(self, name, catchall=True, autojson=True):
        super(Avalon, self).__init__(catchall, autojson)
        self.name = name

    def register_blueprint(self, blueprint):
        for endpoint, route_list in blueprint.url_rules.items():
            for route in route_list:
                rule_all = blueprint.subdomain + blueprint.url_prefix
                route.rule = rule_all + route.rule
                route.app = self
                self.add_route(route)


class Blueprint(object):
    def __init__(self, name, subdomain=None, url_prefix=None):
        self.name = name
        self.subdomain = subdomain
        self.url_prefix = url_prefix
        self.url_rules = {}

    def add_url_rule(self, rule, view_func, methods, endpoint, **options):
        route_list = []
        for method in makelist(methods):
            route = Route(None, rule, method, view_func)
            route_list.append(route)

        self.url_rules.update({endpoint: route_list})


class MethodView(object):
    decorator = []
    methods = []

    @classmethod
    def as_view(cls, name):
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


# like flask
def url_for(name, **options):
    if not isinstance(name, (str, unicode)):
        raise RouteBuildError('The <name> should be a <str> or <unicode>')

    try:
        app, info = name.split(':')
    except ValueError:
        raise RouteBuildError(
            'The <name> should like "<app>:<blueprint>.<endpoint>"')

    try:
        blueprint, endpoint = info.split('.')
    except ValueError:
        raise RouteBuildError(
            'The <name> should like "<app>:<blueprint>.<endpoint>"')


def get_template_path():
    os
    pass


template = functools.partial(
    template, template_lookup=get_template_path())

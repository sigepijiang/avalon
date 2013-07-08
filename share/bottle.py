# -*- coding: utf-8 -*-
from bottle import Bottle
from bottle import Route
from bottle import RouteBuildError
from bottle import makelist


class App(Bottle):
    def __init__(self, name, catchall=True, autojson=True):
        super(App, self).__init__(catchall, autojson)
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
    pass


# like flask
def url_for(name, **options):
    if not isinstance(name, (str, unicode)):
        raise RouteBuildError('The <name> should be a <str> or <unicode>')

    try:
        app, info = name.split(':')
    except ValueError:
        raise RouteBuildError(
            'The <name> should like "<APP>:<blueprint>.<endpoint>"')

    try:
        blueprint, endpoint = info.split('.')
    except ValueError:
        raise RouteBuildError(
            'The <name> should like "<APP>:<blueprint>.<endpoint>"')

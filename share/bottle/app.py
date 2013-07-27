# -*- coding: utf-8 -*-
import os
import functools

from bottle import Bottle
from bottle import Route, Router
from bottle import RouteBuildError
from bottle import makelist
from bottle import template

from share.config import load_yaml
from share.errors import AvalonConfigError
from .utils import get_root_path


class Route(Route):
    def __init__(self, app, rule, method, callback, name=None,
                 plugins=None, skiplist=None, defaults={},
                 **config):
        super(Route, self).__init__(
            app, rule, method, callback,
            name, plugins, skiplist,
            **config)
        self.defaults = defaults


class Router(Router):
    def match(self, environ):
        target, args = super(Router, self).match(environ)
        [args.setdefault(k, v) for k, v in target.defaults.items()]
        return target, args


class Avalon(Bottle):
    def __init__(self, name, catchall=True, autojson=True):
        super(Avalon, self).__init__(catchall, autojson)
        self.name = name
        self.blueprints = []
        self.router = Router()

        try:
            environ = os.environ
            self.config.home_path = environ['BASE']
            self.config.app_name = name
            self.config.environ = environ['AVALON_ENVIRON']
            self.config.app_path = get_root_path(name)

            gloabal_config = load_yaml(
                os.path.join(self.config.home_path, 'avalon.yaml'))
            app_config = load_yaml(
                os.path.join(get_root_path(name), '../app.yaml'))

            default_memcached = gloabal_config['MEMCACHED']
            default_enable_sql_echo = gloabal_config['ENABLE_SQL_ECHO']
            self.config.static_path = os.path.join(
                environ['BASE'], gloabal_config['STATIC_PATH'])

            gloabal_config = gloabal_config['APP_' + name.upper()]
            self.config.enable_sql_echo = gloabal_config.get(
                'ENABLE_SQL_ECHO', default_enable_sql_echo)
            self.config.memcached = gloabal_config.get(
                'MEMCACHED', default_memcached)

            if len(
                set(app_config.keys()) - set(gloabal_config.keys())
            ) < len(app_config):
                raise AvalonConfigError('app设置与global冲突')

            app_config.update(gloabal_config)
            for i in app_config.keys():
                setattr(self.config, i.lower(), app_config[i])
        except KeyError as e:
            raise AvalonConfigError(e)

    def register_blueprint(self, blueprint, url_prefix):
        for endpoint, route_list in blueprint.url_rules.items():
            for route in route_list:
                rule_all = url_prefix or blueprint.url_prefix
                route.rule = rule_all + route.rule
                route.app = self
                self.add_route(route)
        self.blueprints.append(blueprint)


class Blueprint(object):
    def __init__(self, name, subdomain=None, url_prefix=None):
        self.name = name
        self.subdomain = subdomain
        self.url_prefix = url_prefix
        self.url_rules = {}

    def add_url_rule(self, rule, view_func,
                     methods, endpoint, defaults={}, **options):
        route_list = []
        for method in makelist(methods):
            route = Route(
                None, rule, method, view_func, defaults=defaults)
            route_list.append(route)

        self.url_rules.update({endpoint: route_list})


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

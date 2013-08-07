# -*- coding: utf-8 -*-
import os

from bottle import Bottle
from bottle import Route, Router
from bottle import makelist

from share.config import load_yaml
from share.errors import AvalonConfigError, AvalonException
from share.url_map import url_for
from .utils import get_root_path


class Route(Route):
    def __init__(self, app, rule, method, callback, name=None,
                 plugins=None, skiplist=None, defaults={},
                 https=False, **config):
        super(Route, self).__init__(
            app, rule, method, callback,
            name, plugins, skiplist,
            **config)
        self.defaults = defaults
        self.https = https


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
            default_domain = gloabal_config['DOMAIN']

            gloabal_config = gloabal_config['APP_' + name.upper()]
            self.config.enable_sql_echo = gloabal_config.get(
                'ENABLE_SQL_ECHO', default_enable_sql_echo)
            self.config.memcached = gloabal_config.get(
                'MEMCACHED', default_memcached)
            self.config.domain = gloabal_config.get(
                'DOMAIN', default_domain)

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

    def get_url(self, endpoint, **kwargs):
        # TODO: endpoint = <blueprint>.<name>
        # try:
        #     b, n = endpoint.split[':'][-1].split('.')
        # except ValueError:
        #     raise RouteBuildError(
        #         'endpoint should end with <blueprint>:<name>')

        # blueprint = None
        # for bp in self.blueprints:
        #     if bp.name == b:
        #         blueprint = bp
        #         break
        # if not blueprint:
        #     raise RouteBuildError(
        #         'blueprint "%s" not found' % b)

        scheme, subdomain, path = url_for(endpoint, **kwargs)
        return '%s://%s.%s%s' % (
            scheme,
            subdomain,
            self.config.domain,
            path)


class Blueprint(object):
    def __init__(self, name, subdomain=None, url_prefix=None):
        self.name = name
        self.subdomain = subdomain
        self.url_prefix = url_prefix
        self.url_rules = {}

    def add_url_rule(self, rule, view_func,
                     methods, endpoint, defaults={},
                     https=False, **options):
        route_list = []
        endpoint = endpoint or view_func.__name__
        for method in makelist(methods):
            route = Route(
                None, rule, method, view_func, defaults=defaults,
                name=endpoint, https=https)
            route.blueprint = self
            route_list.append(route)

        if self.url_rules.get(endpoint):
            raise AvalonException('the endpoint has been set.')
        self.url_rules[endpoint] = route_list

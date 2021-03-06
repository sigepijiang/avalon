# -*- coding: utf-8 -*-
import os
import requests

from bottle import Bottle, default_app
from bottle import Route, Router
from bottle import makelist

from share.config import load_yaml
from share.utils.base62 import to_url, to_python
from share.errors import AvalonConfigError, AvalonException
from share.url_map import url_for
from share.utils import _static_file
from .utils import get_root_path
from .hooks import fill_session, save_session, db_session_rollback
from .restful import apis


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
    def __init__(self, strict=False):
        super(Router, self).__init__(strict)
        self.add_filter(
            'uid', lambda conf: (r'\d+', to_python, lambda i: str(to_url(i))))

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
        self._init_config(name)
        self._access_token = {}

        # 不知道为什么不能用add_hook
        self.add_hook('before_request', fill_session)
        self.add_hook('before_request', db_session_rollback)
        self.add_hook('after_request', save_session)

        default_app.push(self)

    def _init_config(self, name):
        try:
            environ = os.environ
            self.config.home_path = environ['BASE']
            self.config.environ = environ['AVALON_ENVIRON']
            self.config.app_path = get_root_path(name)
            self.config.app_name = name

            global_config = load_yaml(
                os.path.join(self.config.home_path, 'avalon.yaml'))
            app_config = load_yaml(
                os.path.join(get_root_path(name), '../app.yaml'))
            gloabal_app_config = global_config.pop('APPS')[name.upper()]

            if len(
                set(app_config.keys()) - set(gloabal_app_config.keys())
            ) < len(app_config):
                raise AvalonConfigError('app设置与global冲突')

            app_config.update(gloabal_app_config)
            for i in app_config.keys():
                setattr(self.config, i.lower(), app_config[i])

            global_config.pop('UWSGI')
            nginx_config = global_config.pop('NGINX')
            for i in global_config.keys():
                setattr(self.config, i.lower(), global_config[i])
            self.config.global_port = nginx_config['LISTEN']
        except KeyError as e:
            raise AvalonConfigError(e)

    def register_blueprint(self, blueprint, url_prefix=''):
        for endpoint, route_list in blueprint.url_rules.items():
            for route in route_list:
                rule_all = url_prefix + blueprint.url_prefix
                route.rule = rule_all + route.rule
                route.app = self
                self.add_route(route)
        self.blueprints.append(blueprint)

    def get_url(self, endpoint, **kwargs):
        # TODO: endpoint = <blueprint>.<name> or <name>
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

        return url_for(endpoint, **kwargs)

    def static_file_func(self):
        return lambda path: _static_file(
            self.config.domain, self.config.global_port, path)

    @property
    def access_token(self):
        if not self._access_token:
            url = apis.zeus.oauth2.client._url
            resp = requests.post(url, data=dict(
                client_id=self.config.client_id,
                secret=self.config.client_secret,
            ))
            access_token = resp.json()['result']
            self._access_token = access_token
        return self._access_token['access_token']

    @access_token.setter
    def _set_access_token(self, v):
        self._access_token = v


class Blueprint(object):
    def __init__(self, name, subdomain='www', url_prefix=''):
        self.name = name
        self.subdomain = subdomain
        self.url_prefix = url_prefix
        self.url_rules = {}

    def add_url_rule(self, rule, view_func, methods,
                     endpoint=None, defaults={},
                     https=False, **options):
        route_list = []
        endpoint = endpoint or view_func.__name__
        for method in makelist(map(lambda m: m.upper(), methods)):
            route = Route(
                None, rule, method, view_func, defaults=defaults,
                name=endpoint, https=https)
            route.blueprint = self
            route_list.append(route)

        if self.url_rules.get(endpoint):
            raise AvalonException('the endpoint has been set.')
        self.url_rules[endpoint] = route_list


class APIBlueprint(Blueprint):
    def __init__(self, name):
        from bottle import default_app
        super(APIBlueprint, self).__init__(
            name, 'apis', '/' + default_app().name)


class BackendsBlueprint(Blueprint):
    def __init__(self, name):
        from bottle import default_app
        super(BackendsBlueprint, self).__init__(
            name, 'backends', '/' + default_app().name)

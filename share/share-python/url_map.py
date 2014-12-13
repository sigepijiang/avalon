# -*- coding: utf-8 -*-
import os

import yaml

from share.errors import RouteBuildError
from share.utils import is_file_exists


def _url_bottle_handle(rule, **kwargs):
    from share.framework.bottle import Router
    scheme = 'https' if rule['https'] else 'http'
    subdomain = rule['subdomain']
    rule = rule['rule']
    router = Router()
    router.add(rule, 'GET', lambda i: i, 'target')
    path = router.build('target', **kwargs)
    return scheme, subdomain, path


URL_FACTORY = {
    'bottle': _url_bottle_handle,
}
URL_MAP = {}


def get_url_map(app_name):
    global URL_MAP
    map_file = os.path.join(
        os.environ['BASE'],
        'share/url_maps/%s.yaml' % app_name)
    if not is_file_exists(map_file):
        raise RouteBuildError('app <%s> not avaliable!' % app_name)

    if not URL_MAP.get(app_name, None):
        with open(map_file, 'rb') as f:
            URL_MAP[app_name] = yaml.load(f)
    return URL_MAP[app_name]


def get_endpoint_info(name):
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
    return app, blueprint, endpoint


def url_for(endpoint, **kwargs):
    app, blueprint, name = get_endpoint_info(endpoint)
    url_map = get_url_map(app)
    domain = url_map['domain']
    global_port = url_map['global_port']

    try:
        rule = url_map['blueprints'][blueprint][name]
    except KeyError as e:
        raise RouteBuildError(e)

    app_base = url_map['app_base']
    scheme, subdomain, path = URL_FACTORY[app_base](
        rule, **kwargs)

    if global_port in ('80', 80):
        return '%(scheme)s://%(subdomain)s.%(domain)s%(path)s' % dict(
            scheme=scheme, subdomain=subdomain, domain=domain, path=path)
    return (
        '%(scheme)s://%(subdomain)s.%(domain)s:'
        '%(global_port)s%(path)s') % dict(
            scheme=scheme, subdomain=subdomain,
            domain=domain, path=path, global_port=global_port)

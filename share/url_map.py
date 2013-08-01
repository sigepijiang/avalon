# -*- coding: utf-8 -*-
import os

import yaml
from bottle import RouteBuildError

from share.bottle import Router


def _url_bottle_handle(rule, **kwargs):
    Router()
    pass


URL_FACTORY = {
    'bottle': _url_bottle_handle,
}
URL_MAP = {}


def get_url_map():
    global URL_MAP
    map_file = os.path.join(os.environ['BASE'], 'share/url_map.yaml')
    if not URL_MAP:
        with open(map_file, 'wb') as f:
            URL_MAP = yaml.load(f)
    return URL_MAP


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
    return app, blueprint, name


def url_for(endpoint, **kwargs):
    app, blueprint, name = get_endpoint_info(endpoint)
    url_map = get_url_map()

    try:
        rule = url_map[app][blueprint][name]
    except KeyError:
        raise RouteBuildError('Not found')

    app_name = url_map[app]['app_name']
    return URL_FACTORY[app_name](rule, **kwargs)

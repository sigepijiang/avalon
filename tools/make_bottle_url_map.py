#-*- coding: utf-8 -*-
import sys
import os

import yaml

from share.errors import AvalonException
from share.utils import import_module


def make_url_map():
    print sys.argv
    app_name, app_path, app_type = sys.argv[1:]
    map_file = os.path.join(
        os.environ['BASE'],
        'share/url_maps/%s.yaml' % app_name)
    sys.path.insert(0, app_path)
    app = import_module(app_name).app
    url_map = get_app_url_map(app)

    with open(map_file, 'wb') as f:
        yaml.dump(url_map, f)


def get_app_url_map(app):
    result = {}
    app_type = app.config.app_type
    app_name = app.config.app_name
    app_domain = app.config.domain
    blueprints = app.blueprints
    blueprints = {b.name: b for b in blueprints}
    blueprint_keys = blueprints.keys()
    blueprint_keys.sort()

    result = {
        'app_type': app_type,
        'app_name': app_name,
        'domain': app_domain,
        'blueprints': {},
    }
    for name in blueprint_keys:
        blueprint = blueprints[name]
        result['blueprints'].update({
            name: get_blueprint_url_map(blueprint)})
    return result


def get_blueprint_url_map(blueprint):
    result = {}
    url_rules = blueprint.url_rules
    for endpoint, routes in url_rules.items():
        rule_set = set([i.rule for i in routes])
        if len(rule_set) > 1:
            raise AvalonException(
                'endpoint %s has more than one rules' % endpoint)

        route = routes.pop()
        result.update({endpoint: {
            'rule': route.rule,
            'subdomain': blueprint.subdomain,
            'https': route.https,
        }})
    return result

if __name__ == '__main__':
    make_url_map()

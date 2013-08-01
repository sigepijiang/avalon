#-*- coding: utf-8 -*-
import sys
import os

import yaml

from share.errors import AvalonEnvironError, AvalonException


# copied from django
def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in range(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                             "package")
    return "%s.%s" % (package[:dot], name)


# copied from django
def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]


def get_enbled_apps():
    apps = sys.argv[1:]
    apps.sort()
    return {app: get_app_path(app) for app in apps}


def get_app_path(app_name):
    environ = os.environ
    try:
        base_path = environ['BASE']
    except KeyError:
        raise AvalonEnvironError('BASE is not set')

    dir_path = os.walk(base_path)
    all_app_path = []
    for root, dirs, files in dir_path:
        if 'app.yaml' in files:
            all_app_path.append(root)

    target_app_path = [i for i in all_app_path if app_name in i]
    if len(target_app_path) > 1:
        raise AvalonException('Dumplicate app name %s' % app_name)

    return target_app_path[0]


def make_url_map():
    map_file = os.path.join(os.environ['BASE'], 'share/url_map.yaml')
    app_path_map = get_enbled_apps()
    url_map = {}
    for app_name, app_path in app_path_map.items():
        sys.path.insert(0, app_path)
        app = import_module(app_name).app
        url_map.update({app_name: get_app_url_map(app)})

    with open(map_file, 'wb') as f:
        yaml.dump(url_map, f)


def get_app_url_map(app):
    result = {}
    app_type = app.config.app_type
    app_name = app.config.app_name
    blueprints = app.blueprints
    blueprints = {b.name: b for b in blueprints}
    blueprint_keys = blueprints.keys()
    blueprint_keys.sort()

    result = {'app_type': app_type, 'app_name': app_name}
    for name in blueprint_keys:
        blueprint = blueprints[name]
        result[name] = get_blueprint_url_map(blueprint)
    print result
    return result


def get_blueprint_url_map(blueprint):
    result = {}
    url_rules = blueprint.url_rules
    for endpoint, routes in url_rules.items():
        rule_set = set([i.rule for i in routes])
        if len(rule_set) > 1:
            raise AvalonException(
                'endpoint %s has more than one rules' % endpoint)

        routes = routes.pop()
        result.update({endpoint: {
            'rule': routes.rule,
            'subdomain': blueprint.subdomain,
        }})
    return result

if __name__ == '__main__':
    make_url_map()

#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re

import yaml

from share.errors import AvalonRouteException


APP_BASE_MAP = {
    'bottle': 'uwsgi'
}


def check_rule(rule):
    wrong_list = ['apis', 'backends', 'services']
    if len(rule.rule_tuple) == 0:
        return

    if rule.rule_tuple[0] in wrong_list:
        raise AvalonRouteException(
            '%s begins with %s' % (
                rule.rule, ', '.join(wrong_list)))


def is_regex_rule(value):
    # for <bottle> or <flask>
    if re.match('^.*<.*>.*$', value):
        return True
    return False


class Root(object):
    def __init__(self):
        self.domains = {}
        self.domain_rules = {}

    def add_domain_rules(self, domain, rules):
        self.domains.setdefault(domain, Domain(domain))
        self.domain_rules.setdefault(domain, []).extend(rules)

    def merge(self):
        for domain in self.domains:
            self.domains[domain].add_rules(self.domain_rules[domain])
            self.domains[domain].merge()


class Domain(object):
    def __init__(self, name):
        self.name = name
        self.subdomains = {}

    def add_rules(self, rules):
        for r in rules:
            subdomain = self.subdomains.setdefault(
                r.subdomain, Subdomain(self, r.subdomain))
            subdomain.rules.append(r)

    def merge(self):
        for subdomain in self.subdomains.values():
            subdomain.merge()

    @property
    def app_list(self):
        apps = []
        for s in self.subdomains.values():
            for l in s.locations.values():
                apps.append(l.app)
        return {app.app_name: app for app in apps}.values()


class App(object):
    def __init__(self, app_name, app_base):
        self.app_name = app_name
        self.app_base = APP_BASE_MAP[app_base]


class Subdomain(object):
    def __init__(self, domain, name):
        self.domain = domain
        self.name = name
        self.rules = []
        self.locations = {}
        self.suspicious_url = []

    def merge(self):
        merged_list = []
        to_merge_list = []

        for r in self.rules:
            check_rule(r)
            if len(r.rule_tuple) == 0:
                to_merge_list.append(r)
                continue

            if r.rule_tuple[0] == r.app.app_name:
                r.location_at = 0
                merged_list.append(r)
                continue

            to_merge_list.append(r)

        # check root path
        root_count = len(filter(
            lambda i: len(i.rule_tuple) == 0, to_merge_list))
        if root_count > 1:
            raise AvalonRouteException('There is two root route!')
        root = filter(lambda i: len(i.rule_tuple) == 0, to_merge_list)
        if root:
            to_merge_list.remove(root[0])
            merged_list.append(root[0])

        location_at = 0
        while to_merge_list:
            self._merge_rule(merged_list, to_merge_list, location_at)
            location_at += 1

        self._make_location(merged_list)

    def _merge_rule(self, merged_list, to_merge_list, location_at):
        dealed_list = []
        for r in to_merge_list:
            if len(r.rule_tuple) < location_at:
                raise AvalonRouteException(
                    ('The length of rule <%s> is less than location_at(%s).'
                     'Please find other urls like this.') % (
                         r.rule, location_at))

            for token in r.rule_tuple[:location_at + 1]:
                if is_regex_rule(token):
                    raise AvalonRouteException(
                        'The rule<%s> contains a reges expression.' % r.rule)

            token_diff_app = filter(
                lambda i: (
                    i.rule_tuple[:location_at + 1]
                    == r.rule_tuple[:location_at + 1]
                    and i.app.app_name != r.app.app_name),
                to_merge_list)
            token_count = len(token_diff_app)
            if token_count == 0:
                r.location_at = location_at
                merged_list.append(r)
                dealed_list.append(r)

        [to_merge_list.remove(i) for i in dealed_list]

    def _make_location(self, merged_list):
        self.locations = {
            r.location: Location(
                self,
                name=r.location,
                app=r.app) for r in merged_list}


class Location(object):
    def __init__(self, subdomain, name, app):
        self.subdomain = subdomain
        self.name = name
        self.app = app


class Rule(object):
    def __init__(self, subdomain, https, rule, app_name, app_base):
        self.subdomain = subdomain
        self.https = https
        self.rule = rule
        self.app = App(app_name, app_base)
        self.location_at = -1

    @property
    def rule_tuple(self):
        return self.rule.strip('/').split('/')

    @property
    def location(self):
        return '/%s' % '/'.join(self.rule_tuple[:self.location_at + 1])


def get_url_maps(path, file_list):
    result = {}
    for i in file_list:
        app_name = i.split('.')[0]
        with open(os.path.join(path, i), 'rb') as f:
            result[app_name] = yaml.load(f)
    return result


def get_rule_list(app_config):
    result = []
    app_name = app_config['app_name']
    app_base = app_config['app_base']
    blueprints = app_config['blueprints']
    for subdomain, url_map in blueprints.items():
        for endpoint, url in url_map.items():
            result.append(Rule(
                app_base=app_base, app_name=app_name, **url))
    return result


def build_tree(url_map):
    root = Root()
    for app_name, app_config in url_map.items():
        rules = get_rule_list(app_config)
        domain = app_config['domain']
        root.add_domain_rules(domain, rules)

    root.merge()
    return root


def get_tree():
    environ = os.environ
    base_path = environ['BASE']
    url_config_path = os.path.join(base_path, 'share/url_maps')
    url_yamls = os.path.os.listdir(url_config_path)
    url_map = get_url_maps(url_config_path, url_yamls)
    return build_tree(url_map)


if __name__ == '__main__':
    root = get_tree()

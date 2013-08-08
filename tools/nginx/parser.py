#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""自动生成nginx配置

目前可以生成 upstreams.conf, sites.conf 和 apis.conf 三个配置

这个脚本目前写得挺乱的, 先凑合着用吧. 打算未来重构.

"""

import re
from itertools import chain
from werkzeug.routing import parse_rule, get_converter
from guokr.platform.routing_rules import url_map


class Domain(object):

    def __init__(self, port=None, is_default_server=None,
                 server_names=None, locations=None):
        self.port = port
        self.is_default_server = is_default_server
        self.server_names = server_names
        if locations is None:
            locations = []
        self.locations = locations


class Location(object):

    def __init__(self, appname, type=None):
        self.appname = appname
        self.type = type


class Node(object):

    def __init__(self, string, app=False, is_domain=False,
                 is_regex=False, is_root=False, parent=None):
        self.string = string
        self.app = app
        self.is_domain = is_domain
        self.is_regex = is_regex
        self.is_root = is_root
        self.parent = None
        self.children = []

    def merge_child(self, node):
        if node in self.children:
            return self.children[self.children.index(node)]
        else:
            self.children.append(node)
            if self.app != node.app:
                self.app = False
            return node

    def optimize(self):
        """节点优化

        合并 app 相同, location相似的节点, 展开 app 不同的节点

        Returns: None

        """
        if self.is_root:
            for domain in self.children:
                domain.optimize()

        elif self.is_domain:
            if self.app is False:
                # 下有多个 app 的情况
                children = []
                for loc in self.children:
                    children.extend(loc.optimize_expand())
            else:
                # 只有一个 app 的情况
                children = [Node('/', self.app, parent=self)]
            self.children = children
            children = children[:]
            # 进一步优化, 合并相同前缀的节点
            removed = []
            for child in children:
                for child_cmp in children:
                    if not child.is_regex and \
                       not child_cmp.is_regex and \
                       child_cmp.app == child.app and \
                       child_cmp.string != child.string and \
                       child_cmp.string.startswith(child.string):
                        removed.append(child_cmp)
            for child in removed:
                try:
                    self.children.remove(child)
                except ValueError:
                    pass

    def optimize_expand(self, locprefix=''):
        """展开 app 不同的节点

        Returns: list()

        """
        if self.app is False:
            locprefix += '/' + self.string
            siblings = []
            for subloc in self.children:
                siblings.extend(subloc.optimize_expand(locprefix))
            for sibling in siblings:
                sibling.parent = self.parent
            return siblings

        else:
            location = locprefix + '/'
            if self.is_regex:
                if self.string not in ('.*', '.+'):
                    location = re.escape(location) + self.string
            else:
                location += self.string
            self.string = location
            self.children = []
            return [self]

    def __eq__(self, another):
        return (self.string == another.string and
                self.is_domain == another.is_domain and
                self.is_regex == another.is_regex and
                self.is_root == another.is_root and
                self.parent == another.parent)

    def __repr__(self):
        return 'Node(%s, %s)' % (repr(self.string), repr(self.app))


def yield_nodes(rule):

    app = rule.endpoint.rsplit(':', 1)[0]
    parent = None

    def _build_node(string, parent, is_domain=False):
        yielded = False
        for converter, arguments, variable in parse_rule(string):
            if converter is None:
                for part in variable.split('/'):
                    if part:
                        node = Node(part, app=app,
                                    is_domain=is_domain, parent=parent)
                        yielded = True
                        yield node
                        parent = node
            else:
                convobj = get_converter(rule.map, converter, arguments)
                node = Node(convobj.regex, app=app, is_domain=is_domain,
                            is_regex=True, parent=parent)
                yielded = True
                yield node
                parent = node
        if not yielded:  # / can't be yielded
            yield Node('', app=app, is_domain=is_domain, parent=parent)

    return chain(
        _build_node(rule.subdomain, parent, is_domain=True),
        _build_node(rule.rule.rstrip('/'), parent))


def build_tree():
    root = current = Node('ROOT', is_root=True)
    for rule in url_map.iter_rules():
        for node in yield_nodes(rule):
            if node.is_domain:
                current = root
            current = current.merge_child(node)
    root.optimize()
    return root


if __name__ == '__main__':
    root = build_tree()

#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""自动生成nginx配置

目前可以生成 upstreams.conf, sites.conf 和 apis.conf 三个配置

"""

import os
import shutil
import platform
import multiprocessing

from jinja2 import Environment, FileSystemLoader
from share.config import load_yaml

import parser

BASE = os.environ['BASE']
PWD = os.path.abspath(os.path.dirname(__file__))
JENV = Environment(loader=FileSystemLoader(os.path.join(PWD, 'templates')))
CONF = None


def config():
    global CONF
    if CONF is None:
        CONF = load_yaml(os.path.join(BASE, 'avalon.yaml'))
    return CONF


def render_domain_static(path, domain):
    conf = config()
    file_path = os.path.join(path, 'static.conf')

    base_path = os.environ['BASE']
    alias_path = os.path.join(
        base_path, conf['STATIC_PATH'])
    port = conf['NGINX']['LISTEN']
    is_default_server = False
    site_name = 'static'
    server_names = ['.'.join(['static', domain.name])]
    locations = [dict(
        name='/', app=dict(
            app_type='alias',
            app_alias=alias_path))]
    domain = domain.name
    text = JENV.get_template('site.jinja2').render(
        port=port,
        is_default_server=is_default_server,
        site_name=site_name, server_names=server_names,
        locations=locations, domain=domain)
    writefp(file_path, text)


def render_upstreams():
    conf = config()
    upstreams = []
    for app, appconf in conf.iteritems():
        if not app.startswith('APP_'):
            continue
        ups = {'name': 'app_%s' % app[4:].lower(), 'servers': []}
        host = appconf['HOST']
        if 'JAVA_PORT' in appconf:
            port = appconf['JAVA_PORT']
        else:
            port = appconf['PORT']
        ups['servers'].append('%s:%s' % (host, port))
        ups['port'] = port
        upstreams.append(ups)
    upstreams.sort(key=lambda ups: ups['port'])
    return JENV.get_template('upstreams.jinja2').render(upstreams=upstreams)


def render_nginx_conf(root):
    conf = config()
    workers = multiprocessing.cpu_count()
    events = dict(use='epoll', worker_connections=10240)

    if platform.system() == 'Darwin':
        events['use'] = 'kqueue'

    return (JENV.get_template('nginx.conf.jinja2')
                .render(chroot=chroot(), workers=workers,
                        events=events,
                        port=conf['NGINX']['LISTEN'],
                        domain=conf['DOMAIN'],
                        root=root))


def render_apis_includes(path, root):
    conf = config()
    file_path = os.path.join(path, 'apis_includes')

    port = conf['NGINX']['LISTEN']
    text = JENV.get_template('apis_includes.jinja2').render(
        root=root, port=port,)
    writefp(file_path, text)


def render_static(template):
    return JENV.get_template(template).render()


def render_domain(domain):
    _chroot = chroot()
    domain_config_path = os.path.join(
        _chroot, 'etc/nginx/sites-available', domain.name)
    symlink_path = os.path.join(
        _chroot, 'etc/nginx/sites-enabled', domain.name)
    makedirs(domain_config_path)
    [render_subdomain(
        domain_config_path, s) for s in domain.subdomains.values()]
    symlink(domain_config_path, symlink_path)
    render_domain_static(domain_config_path, domain)


def render_subdomain(path, subdomain):
    conf = config()
    file_path = os.path.join(path, '%s.conf' % subdomain.name)

    port = conf['NGINX']['LISTEN']
    is_default_server = subdomain.name == 'www'
    site_name = subdomain.name
    server_names = ['.'.join([subdomain.name, subdomain.domain.name])]
    locations = subdomain.locations.values()
    domain = subdomain.domain.name
    text = JENV.get_template('site.jinja2').render(
        port=port,
        is_default_server=is_default_server,
        site_name=site_name, server_names=server_names,
        locations=locations, domain=domain)
    writefp(file_path, text)


def chroot():
    chroot = config()['NGINX'].get('CHROOT')
    if not chroot:
        chroot = '/'
    if chroot[0] != '/':
        chroot = os.path.join(BASE, chroot)
    return chroot


def makedirs(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def rmdirs(path):
    shutil.rmtree(path, ignore_errors=True)


def writefp(path, text):
    with open(path, 'wb') as fp:
        print '\033[0;32;1mUpdating %s ...\033[0m' % path
        fp.write(text)


def symlink(src, dst):
    try:
        os.remove(dst)
    except OSError:
        pass
    print '\033[0;32;1mCreating symlink ...\033[0m'
    os.symlink(src, dst)


def install():
    _chroot = chroot()
    nginxbase = os.path.join(_chroot, 'etc/nginx')
    enabled = os.path.join(_chroot, 'etc/nginx/sites-enabled')
    available = os.path.join(_chroot, 'etc/nginx/sites-available')
    rmdirs(nginxbase)
    makedirs(enabled)
    makedirs(available)
    makedirs(os.path.join(_chroot, 'var/run'))
    makedirs(os.path.join(_chroot, 'var/log/nginx'))
    makedirs(os.path.join(_chroot, 'var/lib/nginx/body'))

    root = parser.get_tree()
    [render_domain(i) for i in root.domains.values()]
    render_apis_includes(nginxbase, root)

    writefp(os.path.join(nginxbase, 'nginx.conf'),
            render_nginx_conf(root))

    writefp(os.path.join(nginxbase, 'upstreams.conf'),
            render_upstreams())

    writefp(os.path.join(nginxbase, 'proxy_params'),
            render_static('proxy_params.jinja2'))

    writefp(os.path.join(nginxbase, 'uwsgi_params'),
            render_static('uwsgi_params.jinja2'))

    writefp(os.path.join(nginxbase, 'mime.types'),
            render_static('mime.types.jinja2'))


if __name__ == '__main__':
    install()

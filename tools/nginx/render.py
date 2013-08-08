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
from guokr.platform.config import load_yaml

import parser

BASE = os.environ['BASE']
PWD = os.path.abspath(os.path.dirname(__file__))
JENV = Environment(loader=FileSystemLoader(os.path.join(PWD, 'templates')))
CONF = None


def config():
    global CONF
    if CONF is None:
        CONF = load_yaml(os.path.join(BASE, 'guokr.yaml'))
        #_CONF = conf(
        #    yaml['UNIFIED_PORT'],
        #    'www',
        #    yaml['DOMAIN_NAME'],
        #    os.path.join(os.environ['BASE'], yaml['STATIC_DIR']),
        #    os.path.join(os.environ['BASE'], yaml['MOBILE_STATIC_DIR']),
        #    os.path.join(os.environ['BASE'], yaml['YOUTHPLAN_DIR']),
        #    os.path.join(os.environ['BASE'], yaml['SPECIAL_DIR']),
        #    yaml)
    return CONF


def uwsgi_adapter(app):
    return {'type': 'uwsgi',
            'appname': app}


def proxy_adapter(app):
    return {'type': 'proxy',
            'appname': app}


def static_adapter(app):
    return {'type': 'alias',
            'alias': os.path.join(BASE, config()['STATIC_DIR'])}


def mstatic_adapter(app):
    return {'type': 'alias',
            'alias': os.path.join(BASE, config()['MOBILE_STATIC_DIR'])}


def youthplan_adapter(app):
    return {'type': 'alias',
            'alias': os.path.join(BASE, config()['YOUTHPLAN_DIR'])}

def special_adapter(app):
    return {'type': 'alias',
            'alias': os.path.join(BASE, config()['SPECIAL_DIR'])}

def apis_adapter(app):
    return {'type': 'include',
            'module': 'apis_includes.conf'}


def adapter(app):
    if app.endswith(':apis'):
        app = ':apis'  # 所有的 apis 都是相同的
    return {
        ':apis': apis_adapter,
        ':mstatic': mstatic_adapter,
        ':static': static_adapter,
        ':youthplan': youthplan_adapter,
        ':special': special_adapter,
        'galahad': proxy_adapter,
        'bedivere': proxy_adapter,
        'lancelot': proxy_adapter,
    }.get(app, uwsgi_adapter)(app)


def render_site(site):
    conf = config()
    port = conf['UNIFIED_PORT']
    is_default_server = site.string == 'www'
    server_names = ['%s.%s' % (site.string, conf['DOMAIN_NAME'])]

    # By zy
    if site.string == 'liuyan':
        server_names.append('www.liuyanbaike.com')
        server_names.append('liuyanbaike.com')
    locations = []
    site_name = site.string
    for child in site.children:
        loc = adapter(child.app)
        loc['pattern'] = child.string
        if child.is_regex:
            loc['op'] = '~'
        else:
            # 尼玛正则表达式怎么转成易于识别的文件名啊
            loc['name'] = \
                '%s%s' % \
                (site_name, child.string.replace('/', '.'))
            loc['name'] = loc['name'].strip('.')
        locations.append(loc)
    return JENV.get_template('site.jinja2').render(
        port=port, is_default_server=is_default_server,
        site_name=site_name, server_names=server_names, locations=locations)


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


def render_apis_includes(site):
    conf = config()
    locations = []
    port = conf['UNIFIED_PORT']
    for child in site.children:
        loc = adapter(child.app)
        loc['pattern'] = child.string
        if child.is_regex:
            loc['op'] = '~'
        else:
            # 尼玛正则表达式怎么转成易于识别的文件名啊
            loc['name'] = \
                'apis_include/%s%s' % \
                (child.app, child.string.replace('/', '.'))
            loc['name'] = loc['name'].strip('.')
        locations.append(loc)
    servname = '%s.%s' % (site.string, conf['DOMAIN_NAME'])
    return (JENV.get_template('apis_includes.jinja2')
                .render(locations=locations,
                        servname=servname, port=port))


def render_nginx_conf():
    conf = config()
    workers = multiprocessing.cpu_count()
    events = dict(use='epoll', worker_connections=10240)

    if platform.system() == 'Darwin':
        events['use'] = 'kqueue'

    return (JENV.get_template('nginx.conf.jinja2')
                .render(chroot=chroot(), workers=workers,
                        events=events,
                        unified_port=conf['UNIFIED_PORT'],
                        domain_name=conf['DOMAIN_NAME']))


def render_static(template):
    return JENV.get_template(template).render()


def render_m_url_adapters():
    conf = config()
    domain = conf['DOMAIN_NAME']
    port = conf['UNIFIED_PORT']
    mobile_site = 'm'
    mobile_site_root = '%s.%s%s' % (mobile_site,
                                    domain,
                                    ((':' + str(port)) if port != 80 else ''))
    return (JENV.get_template('m_url_adapters.jinja2')
                .render(mobile_site_root=mobile_site_root))


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

    writefp(os.path.join(nginxbase, 'nginx.conf'),
            render_nginx_conf())

    writefp(os.path.join(nginxbase, 'upstreams.conf'),
            render_upstreams())

    writefp(os.path.join(nginxbase, 'proxy_params'),
            render_static('proxy_params.jinja2'))

    writefp(os.path.join(nginxbase, 'uwsgi_params'),
            render_static('uwsgi_params.jinja2'))

    writefp(os.path.join(nginxbase, 'mime.types'),
            render_static('mime.types.jinja2'))

    root = parser.build_tree()
    for site in root.children:
        writefp(os.path.join(available, 'site_%s.conf' % site.string),
                render_site(site))
        symlink('../sites-available/site_%s.conf' % site.string,
                os.path.join(enabled, 'site_%s.conf' % site.string))

        if site.string == 'apis':
            writefp(os.path.join(nginxbase, 'apis_includes.conf'),
                    render_apis_includes(site))
        elif site.string == 'www':
            writefp(os.path.join(nginxbase, 'm_url_adapters.conf'),
                    render_m_url_adapters())


if __name__ == '__main__':
    install()

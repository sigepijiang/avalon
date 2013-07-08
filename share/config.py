# -*- coding: utf-8 -*-
"""
配置管理模块
~~~~~~~~~~~~

从 app.yaml 中载入当前 app 的配置, 并写入对应的 app 实例中.

"""
import os
import yaml
import socket

from share.errors import AvalonException
from share.errors import AvalonEnvironError


class ConfigurationError(AvalonException):
    pass


def load_yaml(yamlfile):
    try:
        environ = os.environ['AVALON_ENVIRON']
    except KeyError:
        raise AvalonEnvironError(
            'Environment variable AVALON_ENVIRON is not provided')
    with open(yamlfile, 'rb') as fp:
        conf = yaml.load(fp.read())
    host_conf = 'HOST-%s' % socket.gethostname()

    print conf
    if host_conf in conf:
        return conf[host_conf]
    try:
        return conf[environ]
    except KeyError:
        raise ConfigurationError(
            ('The config file %s does not provide '
             'environment support of %s') % (yamlfile, environ))

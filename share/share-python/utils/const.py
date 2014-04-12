#-*- coding: utf-8 -*-
import os
import socket

from share.config import load_yaml


_env = os.environ
_config = load_yaml(os.path.join(_env['BASE'], 'avalon.yaml'))


namespace = _config['NAMESPACE']
domain = _config['DOMAIN']
hostname = socket.gethostname()

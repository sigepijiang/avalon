#-*- coding: utf-8 -*-
import os

from share.config import load_yaml


_env = os.environ
_config = load_yaml(os.path.join(_env['BASE'], 'avalon.yaml'))


namespace = _config['NAMESPACE']

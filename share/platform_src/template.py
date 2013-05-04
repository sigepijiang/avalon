# -*- coding: utf-8 -*-
import functools

from bottle import view, Jinja2Template
from bottle import request

from settings import INSTALLED_APPS
from settings import PRIVATE_APPS
from settings import DOMAIN
from settings import SYS_TITLE


sys_env = {
    'apps': INSTALLED_APPS,
    'private_apps': PRIVATE_APPS,
    'domain': DOMAIN,
    'sys_title': SYS_TITLE,
}


def static_file(path):
    return '/static/%s' % path


jinja2_view = functools.partial(
    view,
    template_adapter=Jinja2Template,
    request=request,
    sys_env=sys_env,
    static_file=static_file,
)

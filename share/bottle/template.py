# -*- coding: utf-8 -*-
import functools

from bottle import view, Jinja2Template
from bottle import request

from settings import INSTALLED_APPS
from settings import PRIVATE_APPS
from settings import DOMAIN
from settings import SYS_TITLE
import markdown2


def login_required():
    pass


CONTENT_CONVERTER = {
    'md': markdown2.markdown,
    'org': '',
}


def content2html(func):
    def call_f(*args, **kwargs):
        result = func(*args, **kwargs)

        content = result.get('content')
        file_type = result.get('file_type')
        content = CONTENT_CONVERTER[file_type](content)
        result['content'] = content

        return result
    return call_f


def org2html():
    pass


def markdown2html(func):
    def call_f(*args, **kwargs):
        result = func(*args, **kwargs)

        content = result.get('content')
        content = markdown2.markdown(content)
        result['content'] = content

        return result
    return call_f


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

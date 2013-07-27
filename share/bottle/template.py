# -*- coding: utf-8 -*-
import os
import functools

from bottle import view, Jinja2Template
from bottle import request
from bottle import default_app

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


def get_template_path():
    app = default_app()
    base_templates = os.path.join(app.home_path, 'share/bottle/templates')
    app_templates = os.path.join(app.app_path, 'templates')
    return [base_templates, app_templates]


jinja2_view = functools.partial(
    view,
    template_adapter=Jinja2Template,
    request=request,
    template_lookup=get_template_path()
)

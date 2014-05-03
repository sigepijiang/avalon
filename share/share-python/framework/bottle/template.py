# -*- coding: utf-8 -*-
import os

from bottle import default_app, request
from jinja2 import Environment, FileSystemLoader

from share.url_map import url_for
from .user import user_meta


jinja2_env = None


# default for jinja2
def get_template_path():
    app = default_app()
    base_templates = os.path.join(
        app.config.home_path,
        'share/share-python/templates/jinja2')
    app_templates = os.path.join(app.config.app_path, 'templates')
    return [base_templates, app_templates]


def init_jinja2():
    global jinja2_env

    cur_app = default_app()

    jinja2_env = Environment(
        loader=FileSystemLoader(get_template_path()))
    jinja2_env.globals.update(
        static_file=cur_app.static_file_func(),
        request=request, url_for=url_for, user_meta=user_meta)


# DONT'T USE the view, template or Jinja2Template of bottle.
# It can't auto reload.
def view(tmp_name):
    def decorator_f(func):
        def call_f(*args, **kwargs):
            global jinja2_env

            if not jinja2_env:
                init_jinja2()

            return jinja2_env.get_template(
                tmp_name).render(
                    func(*args, **kwargs) or {})
        return call_f
    return decorator_f


def render_template(tmp_name, **kwargs):
    if not jinja2_env:
        init_jinja2()
    return jinja2_env.get_template(tmp_name).render(**kwargs)

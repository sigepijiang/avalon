# -*- coding: utf-8 -*-
import os

from bottle import default_app
from jinja2 import Environment, FileSystemLoader


# default for jinja2
def get_template_path():
    app = default_app()
    base_templates = os.path.join(
        app.config.home_path,
        'share/share-python/templates/jinja2')
    app_templates = os.path.join(app.config.app_path, 'templates')
    return [base_templates, app_templates]


jinja2_env = None


# DONT'T USE the view, template or Jinja2Template of bottle.
# It can't auto reload.
def view(tmp_name):
    def decorator_f(func):
        def call_f(*args, **kwargs):
            global jinja2_env

            if not jinja2_env:
                jinja2_env = Environment(
                    loader=FileSystemLoader(get_template_path()))
            return jinja2_env.get_template(
                tmp_name).render(
                    func(*args, **kwargs))
        return call_f
    return decorator_f

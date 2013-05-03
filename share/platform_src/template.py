# -*- coding: utf-8 -*-

import functools

from bottle import view, Jinja2Template
from bottle import request


jinja2_view = functools.partial(
    view,
    template_adapter=Jinja2Template,
    request=request,
)

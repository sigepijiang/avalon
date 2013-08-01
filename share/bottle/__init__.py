# -*- coding: utf-8 -*-
from bottle import default_app, cached_property

from .app import Avalon, Blueprint, url_for, Router
from .view import MethodView, content2html
from .errors import NotFound, BadRequet
from .template import Jinja2Template, view

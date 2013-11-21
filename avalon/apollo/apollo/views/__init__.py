#-*- coding: utf-8 -*-

from share.framework.bottle.app import Blueprint

from .home import HomeView, AboutView

blueprint_www = Blueprint('www', subdomain='www')

blueprint_www.add_url_rule(
    '/', view_func=HomeView.as_view(), methods=['GET'],
    endpoint='main'
)

blueprint_www.add_url_rule(
    '/about', view_func=AboutView.as_view(), methods=['GET'],
    endpoint='about'
)

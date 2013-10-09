#-*- coding: utf-8 -*-

from share.bottle.app import Blueprint

from .home import HomeView

blueprint_www = Blueprint('www', subdomain='www')

blueprint_www.add_url_rule(
    '/', view_func=HomeView.as_view(), methods=['GET'],
    endpoint='main'
)

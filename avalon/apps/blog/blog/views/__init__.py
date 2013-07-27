#-*- coding: utf-8 -*-
from share.bottle.app import Blueprint

from .www import TextView, TextRedirectView

blueprint_www = Blueprint('www', subdomain='www')

blueprint_www.add_url_rule(
    '/<blog_id:int>/',
    view_func=TextView.as_view(),
    methods=['GET'],
    endpoint='main')
blueprint_www.add_url_rule(
    '/<file_name>.<file_type>/',
    view_func=TextRedirectView.as_view(),
    methods=['GET'],
    endpoint='redirect',)

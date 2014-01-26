#-*- coding: utf-8 -*-
from share.framework.bottle.app import Blueprint

from .blog import BlogView, TextView
from .index import IndexView

blueprint_www = Blueprint('www', subdomain='www')

blueprint_www.add_url_rule(
    '/<blog_id:int>/',
    view_func=BlogView.as_view(),
    methods=['GET'],
    endpoint='blog')
blueprint_www.add_url_rule(
    '/<file_name>.<file_type>/',
    view_func=TextView.as_view(),
    methods=['GET'],
    endpoint='blog_redirect',)
blueprint_www.add_url_rule(
    '/',
    view_func=IndexView.as_view(),
    methods=['GET'],
    endpoint='main',
)

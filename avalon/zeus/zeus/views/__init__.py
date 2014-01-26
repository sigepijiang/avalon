#-*- coding: utf-8 -*-
from share.framework.bottle.app import Blueprint

from .login import SigninView, SignUpView

blueprint_account = Blueprint('account', subdomain='account')

blueprint_account.add_url_rule(
    '/signin/',
    view_func=SigninView.as_view(),
    methods=['GET', 'POST'],
    endpoint='login')
blueprint_account.add_url_rule(
    '/signup/',
    view_func=SignUpView.as_view(),
    methods=['GET', 'POST'],
    endpoint='signup')

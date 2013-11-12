#-*- coding: utf-8 -*-
from share.bottle.app import Blueprint

from .auth import AuthView

blueprint_account = Blueprint('account', subdomain='account')

blueprint_account.add_url_rule(
    '/',
    view_func=AuthView.as_view(),
    methods=['GET', 'POST'],
    endpoint='main')

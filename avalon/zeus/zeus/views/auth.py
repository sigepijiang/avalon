#-*- coding: utf-8 -*-

from share.bottle import MethodView, view

from zeus.models import AccountModel


class AuthView(MethodView):
    @view('')
    def get(self):
        pass

    @property
    def post_template():
        return

    def post(self):

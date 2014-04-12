#-*- coding: utf-8 -*-

from share.framework.bottle import MethodView, view


class ProfileView(MethodView):
    @view('i.html')
    def get(self, ukey):
        return {}

#-*- coding: utf-8 -*-

from share.bottle import MethodView, view


class HomeView(MethodView):
    @view('home.html')
    def get(self):
        return {}

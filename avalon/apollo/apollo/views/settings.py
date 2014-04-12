#-*- coding: utf-8 -*-

from share.framework.bottle import MethodView, view


class SettingsView(MethodView):
    @view('settings.html')
    def get(self, ukey):
        return {}

# -*- coding: utf-8 -*-

from share.restful import RESTfulAPI


class AuthAPI(RESTfulAPI):
    path = '/auth'
    methods = ['GET', 'POST', 'PUT']

    def get(self):
        return

    def create(self):
        return

    def update(self):
        return
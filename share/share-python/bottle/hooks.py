# -*- coding: utf-8 -*-

from bottle import request


def fill_user_data():
    user = {}
    request.user = user

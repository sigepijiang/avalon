#-*- coding: utf-8 -*-

from share.framework.bottle import APIBlueprint

from .auth import AuthAPI

bp_apis = APIBlueprint('apis')
AuthAPI.attach_to(bp_apis)

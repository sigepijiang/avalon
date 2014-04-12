#-*- coding: utf-8 -*-

from share.framework.bottle import APIBlueprint

from .oauth2 import ClientOAuthAPI, UserOAuthAPI

bp_apis = APIBlueprint('apis')
ClientOAuthAPI.attach_to(bp_apis)
UserOAuthAPI.attach_to(bp_apis)

# -*- coding: utf-8 -*-
import json
import time
import uuid

from share.utils.const import namespace
from share.framework.bottle.restful import RESTfulOpenAPI
from share.framework.bottle.engines import memory
from share.framework.bottle.restful.validator import resful_validator

from zeus.models import ClientModel
from . import forms


CLIENT_ACCESS_TOKEN_TIMEOUT = 60 * 60 * 24 * 365
USER_ACCESS_TOKEN_TIMEOUT = 60 * 60 * 24 * 90


class ClientOAuthAPI(RESTfulOpenAPI):
    path = '/oauth2/client'
    methods = ['GET', 'POST', 'PUT']

    def get(self):
        return

    @resful_validator(forms.client_id, forms.secret)
    def create(self, client_id, secret):
        client = ClientModel.query.filter(
            ClientModel.id == client_id,
            ClientModel.secret == secret,
        ).first()
        if not client:
            raise

        time_now = time.time()
        access_token = uuid.uuid3(
            uuid.UUID(namespace), '%s@%s' % (client_id, time_now)).hex

        # time_now = time.mktime(datetime.datetime.now().timetuple())
        access_token_info = dict(
            access_token=access_token,
            expired_in=CLIENT_ACCESS_TOKEN_TIMEOUT,
            date_created=time_now,
            date_expired=time_now + CLIENT_ACCESS_TOKEN_TIMEOUT,
        )
        memory.memcached.set(
            'ACCESS_TOKEN::%s' % access_token,
            json.dumps(access_token_info),
            # memcached 脑残啊, time < 30d 是相对时间, time > 30d 是绝对时间
            time=time_now + CLIENT_ACCESS_TOKEN_TIMEOUT,
        )
        return access_token_info

    def update(self):
        return

    def delete(self):
        return


class UserOAuthAPI(RESTfulOpenAPI):
    path = '/oauth2/user'
    methods = ['GET', 'POST', 'PUT']

    def get(self):
        return

    def create(self, ukey):
        time_now = time.time()
        access_token = uuid.uuid3(
            uuid.UUID(namespace), '%s@%s' % (ukey, time_now)).hex
        access_token_info = dict(
            access_token=access_token,
            expired_in=USER_ACCESS_TOKEN_TIMEOUT,
            date_created=time_now,
            date_expired=time_now + USER_ACCESS_TOKEN_TIMEOUT,
        )
        memory.memcached.set(
            'ACCESS_TOKEN::%s' % access_token,
            json.dumps(access_token_info),
            time=USER_ACCESS_TOKEN_TIMEOUT,
        )
        return access_token_info

    def update(self):
        return

# -*- coding: utf-8 -*-
import json
from bottle import request

from share.restful.base import RESTfulBaseAPI
from share.framework.bottle.engines import memory
from share.framework.bottle.errors import Unauthorized

METHOD_MAP = {
    'get': 'get',
    'post': 'create',
    'put': 'update',
    'delete': 'delete',
}


class RESTfulAPI(RESTfulBaseAPI):
    def implement(self):
        pass

    def before_request(self, meth):
        for f in self.hooks.get('before_request', []):
            if callable(f):
                f(meth)
            else:
                raise


    def after_request(self, meth):
        for f in self.hooks.get('after_request', []):
            if callable(f):
                f(meth)
            else:
                raise

    def authorize(self):
        params = (
            request.forms if request.method == 'POST'
            else request.query
        )
        access_token = params.get('access_token')
        if not access_token:
            raise

        access_token_info = json.loads(memory.memcached.get(
            'ACCESS_TOKEN::%s' % access_token
        ) or '{}')
        if not access_token_info:
            raise

        ukey = access_token_info.get('ukey')
        if ukey:
            request.ukey = ukey

        client_id = access_token_info.get('client_id')
        if client_id:
            request.client_id

    def dispatch_request(self, *args, **kwargs):
        request.session = None
        return super(RESTfulAPI, self).dispatch_request(
            *args, **kwargs)


class RESTfulOpenAPI(RESTfulAPI):
    pass


class RESTfulBackendAPI(RESTfulAPI):
    pass

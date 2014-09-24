#-*- coding: utf-8 -*-
from bottle import request

from share.restful.validator import resful_validator
from share.framework.bottle.errors import APIBadRequest


class resful_validator(resful_validator):
    def __init__(self, *args, **kwargs):
        super(resful_validator, self).__init__(None, *args, **kwargs)

    def _get_params(self):
        if 'application/json' in request.environ.get('CONTENT_TYPE', ''):
            try:
                return request.json
            except:
                pass

        params = (
            request.forms if request.method.upper() == 'POST'
            else request.query
        )
        result = {}
        for i in params:
            if i in ['access_token']:
                continue
            if len(params.getlist(i)) > 1:
                result[i] = params.getlist(i)
            else:
                result[i] = params.getone(i)
        return result

    def _raise(self, errors):
        raise APIBadRequest(errors)

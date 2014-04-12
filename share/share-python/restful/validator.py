#-*- coding: utf-8 -*-
from functools import wraps

import voluptuous


class resful_validator(object):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request

        validators = {}
        for item in args:
            assert isinstance(item, dict)
            for key, value in item.items():
                validators[key] = value

        for key, value in kwargs.items():
            validators[key] = value
        self.validators = validators

    def __call__(self, func):
        @wraps(func)
        def call_f(*args, **kwargs):
            params = self._get_params()
            params, errors = self._validate(params)
            kwargs.update(params)
            return func(*args, **kwargs)
        return call_f

    def _validate(self, params):
        result = {}
        errors = {}
        schema = voluptuous.Schema(self.validators)
        result.update(schema(params))
        return result, errors

    def _get_params(self):
        raise NotImplementedError()

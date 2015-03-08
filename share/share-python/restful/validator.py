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

            if errors:
                self._raise(errors)

            kwargs.update(params)
            return func(*args, **kwargs)
        return call_f

    def _validate(self, params):
        result = {}
        errors = {}
        schema = voluptuous.Schema(self.validators)
        try:
            result.update(schema(params))
        except voluptuous.MultipleInvalid as error_group:
            for e in error_group.errors:
                errors[e.path[0].schema] = e.message
        return result, errors

    def _get_params(self):
        raise NotImplementedError()

    def _raise(self, errors):
        raise NotImplementedError()

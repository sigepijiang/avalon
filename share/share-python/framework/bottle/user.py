# -*- coding: utf-8 -*-
import json

from .restful import backends
from .engines import memory


def user_meta(*ukey_list):
    if len(ukey_list) == 0:
        return None

    if len(ukey_list) == 1:
        return _load_user_meta(ukey_list[0])

    result = {}
    for ukey in ukey_list:
        result['ukey'] = _load_user_meta(ukey)
    return result


def _load_user_meta(ukey):
    result = json.loads(memory.memcached.get('USER::%s' % ukey) or '{}')
    if not result:
        result = backends.apollo.user.get(ukey=ukey)
        memory.memcached.set(
            'USER::%s' % ukey, json.dumps(result or {}))
    return result


# TODO: apollo 的user backends应该支持一次取多个user信息
def preload_user_meta(field='ukey', *ukey_list):
    for obj in ukey_list:
        if isinstance(obj, (str, unicode)):
            _load_user_meta(obj)

        if hasattr(obj, field):
            _load_user_meta(getattr(obj, field))

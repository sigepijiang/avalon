# -*- coding: utf-8 -*-
import os
import codecs
from functools import wraps

from share.framework.bottle.errors import NotFound
from share.framework.bottle.template import get_template_path
from share.utils.markdown import markdown

CONTENT_CONVERTER = {
    'md': markdown,
    'org': '',
}


def content2html(func):
    @wraps(func)
    def call_f(*args, **kwargs):
        result = func(*args, **kwargs)

        # 固定寻找<app>/templates/(md|org)/下的文件
        template_path = get_template_path()[1]
        file_name = result.pop('file_name')
        file_type = result.pop('file_type')

        full_path = os.path.join(
            template_path, file_type, file_name + '.' + file_type)
        if not os.path.exists(full_path):
            raise NotFound('页面不存在')

        with codecs.open(full_path, 'r', 'utf-8') as f:
            content = f.read()
        content = CONTENT_CONVERTER[file_type](content)
        result['content'] = content
        return result
    return call_f


def auto_signin(func):
    setattr(func, 'auto_signin', True)
    return func


def signin_required(func):
    setattr(func, 'signin_required', True)
    return func


def authorization_required(func):
    setattr(func, 'authorization_required', True)
    return func

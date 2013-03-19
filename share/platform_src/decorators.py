#-*- coding: utf-8 -*-

import markdown2

from settings import MARKDOWN_PATH
from settings import APP_PATH


def login_required():
    pass

def markdown2html(func):
    def call_f(*args, **kwargs):
        result = func(*args, **kwargs)

        content = result.get('content')
        content = markdown2.markdown(content)
        result['content'] = content

        return result
    return call_f

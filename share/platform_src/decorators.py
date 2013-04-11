#-*- coding: utf-8 -*-

import markdown2


def login_required():
    pass


def content2html():
    pass

def org2html():
    pass

def markdown2html(func):
    def call_f(*args, **kwargs):
        result = func(*args, **kwargs)

        content = result.get('content')
        content = markdown2.markdown(content)
        result['content'] = content

        return result
    return call_f

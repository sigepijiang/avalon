#-*- coding: utf-8 -*-

import markdown2


def login_required():
    pass


CONTENT_CONVERTER = {
        'md': markdown2.markdown,
        'org': '',
        }


def content2html(func):
    def call_f(*args, **kwargs):
        result = func(*args, **kwargs)

        content = result.get('content')
        file_type = result.get('file_type')
        content = CONTENT_CONVERTER[file_type](content)
        result['content'] = content

        return result
    return call_f


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

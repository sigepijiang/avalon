#-*- coding: utf-8 -*-

import codecs

from bottle import route, get, post, redirect
from bottle import request
from bottle import url
from bottle import HTTPError
from bottle import jinja2_view as view
from sqlalchemy import func

from platform_src.decorators import markdown2html
from platform_src.utils import is_file_exists
from settings import MARKDOWN_PATH

from . import APP_NAME
from . import Blog


@get('/<app_name:re:%s>/<blog_id:int>/' % APP_NAME, name='blog.page')
@view('blog')
@markdown2html
def blog(app_name, blog_id):
    blog = Blog.query().filter(Blog.id==blog_id).first()

    if not blog:
        raise HTTPError(404)

    file_path = '/'.join([blog.file_path, blog.file_name])
    file_type = blog.file_name.split('.')[:-1]
    if not is_file_exists(file_path):
        raise HTTPError(404)

    content = codecs.open(file_path, 'r', encoding='utf-8').read()
    return dict(content=content, file_type=file_type)


@get('/<app_name:re:%s>/<file_name>.<file_type>/' % APP_NAME, name='blog.redirect')
def redirect_to_blog(app_name, file_name, file_type):
    file_name += '.' + file_type
    blog = Blog.query().filter(Blog.file_name==file_name).first()
    if not blog:
        if is_file_exists('/'.join([MARKDOWN_PATH, APP_NAME, file_name])):
            blog = Blog.create(
                    file_path='/'.join([MARKDOWN_PATH, APP_NAME]),
                    file_name=file_name)
        else:
            raise HTTPError(404)

    return redirect(url('blog.page', app_name=APP_NAME, blog_id=blog.id))

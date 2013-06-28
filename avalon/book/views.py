#-*- coding: utf-8 -*-

import codecs

from bottle import get, redirect
from bottle import url
from bottle import HTTPError
from bottle import jinja2_view as view

from platform_src.decorators import content2html
from platform_src.utils import is_file_exists
from settings import MARKDOWN_PATH

from . import APP_NAME
from . import Book


@get('/<app_name:re:%s>/<book_id:int>/' % APP_NAME, name='book.page')
@view('book')
@content2html
def book(app_name, book_id):
    book = Book.query().filter(Book.id==book_id).first()

    if not book:
        raise HTTPError(404)

    file_path = '/'.join([book.file_path, book.file_name])
    file_type = book.file_name.split('.')[:-1]
    if not is_file_exists(file_path):
        raise HTTPError(404)

    content = codecs.open(file_path, 'r', encoding='utf-8').read()
    return dict(content=content, file_type=file_type)


@get('/<app_name:re:%s>/<file_name>.<file_type>/' % APP_NAME, name='book.redirect')
def redirect_to_book(app_name, file_name, file_type):
    file_name += '.' + file_type
    book = Book.query().filter(Book.file_name==file_name).first()
    if not book:
        if is_file_exists('/'.join([MARKDOWN_PATH, APP_NAME, file_name])):
            book = book.create(
                    file_path='/'.join([MARKDOWN_PATH, APP_NAME]),
                    file_name=file_name)
        else:
            raise HTTPError(404)

    return redirect(url('book.page', app_name=APP_NAME, book_id=book.id))

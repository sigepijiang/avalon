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
from . import Work


@get('/<app_name:re:%s>/<work_id:int>/' % APP_NAME, name='work.page')
@view('work')
@markdown2html
def work(app_name, work_id):
    work = Work.query().filter(Work.id==work_id).first()

    if not work:
        raise HTTPError(404)

    file_path = '/'.join([work.file_path, work.file_name])
    file_type = work.file_name.split('.')[:-1]
    if not is_file_exists(file_path):
        raise HTTPError(404)

    content = codecs.open(file_path, 'r', encoding='utf-8').read()
    return dict(content=content, file_type=file_type)


@get('/<app_name:re:%s>/<file_name>.<file_type>/' % APP_NAME, name='work.redirect')
def redirect_to_work(app_name, file_name, file_type):
    file_name += '.' + file_type
    work = Work.query().filter(Work.file_name==file_name).first()
    if not work:
        if is_file_exists('/'.join([MARKDOWN_PATH, APP_NAME, file_name])):
            work = Work.create(
                    file_path='/'.join([MARKDOWN_PATH, APP_NAME]),
                    file_name=file_name)
        else:
            raise HTTPError(404)

    return redirect(url('work.page', app_name=APP_NAME, work_id=work.id))

# -*- coding: utf-8 -*-
import simplejson

from bottle import request, response

from share.session import Session
from share.engines import memory


def fill_session():
    session = Session(request.cookies.session_id)
    session.update(simplejson.loads(
        memory.memcached.get(session.session_id) or '{}'))
    request.session = session


def save_session():
    memory.memcached.set(
        request.session.session_id,
        simplejson.dumps(request.session))
    response.set_cookie('session_id', request.session.session_id)

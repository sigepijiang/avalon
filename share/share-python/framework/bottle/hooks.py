# -*- coding: utf-8 -*-
import simplejson

from bottle import request, response

from share.session import Session
from share.framework.bottle.engines import memory


def mc_session_id(request):
    return 'SESSION::%s' % request.cookies.session_id


def fill_session():
    session = Session(request, request.cookies.session_id)
    session.update(simplejson.loads(
        memory.memcached.get(mc_session_id(request)) or '{}'))
    request.session = session
    request.ukey = session.get('ukey', None)


def save_session():
    if request.session:
        from bottle import default_app
        app = default_app()

        memory.memcached.set(
            mc_session_id(request),
            simplejson.dumps(request.session))
        response.set_cookie(
            'session_id', request.session.session_id,
            domain=app.config.domain, path='/'
        )

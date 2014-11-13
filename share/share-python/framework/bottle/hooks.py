# -*- coding: utf-8 -*-
import simplejson

from bottle import request, response

from share.session import Session
from share.framework.bottle.engines import memory
from share.framework.bottle.engines import db


def mc_session_id(session_id):
    return 'SESSION::%s' % session_id


def fill_session():
    session = Session(request, request.cookies.session_id)
    session.update(simplejson.loads(
        memory.memcached.get(mc_session_id(session.session_id)) or '{}'))

    request.ukey = session.get('ukey', None)


def save_session():
    if request.session is None:
        return

    from bottle import default_app
    app = default_app()

    memory.memcached.set(
        mc_session_id(request.session.session_id),
        simplejson.dumps(request.session or {}))
    response.set_cookie(
        'session_id', request.session.session_id,
        domain=app.config.domain, path='/'
    )


def db_session_rollback():
    db.session.rollback()

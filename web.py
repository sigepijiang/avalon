#-*- coding: utf-8 -*-
import share

import argparse
import importlib

from bottle import app
from bottle import run
from bottle import route
from bottle import static_file
from beaker.middleware import SessionMiddleware

from settings import STATIC_ROOT
from settings import APP_PATH
from settings import INSTALLED_APPS
from settings import SERVER_CONFIG
from platform_src.engines import db


@route('/static/<path:path>')
def static_files(path):
    return static_file(path, STATIC_ROOT)


def add_apps():
    for cur_app in INSTALLED_APPS:
        app_full_name = '.'.join([APP_PATH, cur_app])
        importlib.import_module(app_full_name, APP_PATH)


def init_app():
    # session settings
    session_opts = {
        'session.type': 'file',
        'session.cookie_expires': 300,
        'session.data_dir': './session',
        'session.auto': True
    }
    cur_app = SessionMiddleware(app(), session_opts)

    add_apps()

    run(app=cur_app, **SERVER_CONFIG)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Options for Avalon:')
    parser.add_argument('-d', '--deploy', action='store_true', default=False)
    parser.add_argument('-D', '--syncdb', action='store_true', default=False)

    args = parser.parse_args()
    if args.syncdb:
        add_apps()
        #db.Model.metadata.drop_all(db.engine)
        db.Model.metadata.create_all(db.engine)

    if args.deploy:
        init_app()

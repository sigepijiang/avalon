#-*- coding: utf-8 -*-
import os

VERSION = '0.0.1'

PATH = os.path.join(os.getcwd(), os.path.dirname(__file__))

DATABASE = 'sqlite:///%s/data.db' % '/'.join([PATH, 'db'])

STATIC_ROOT = PATH + '/static'
MARKDOWN_PATH = PATH + '/views/markdown'

APP_PATH = 'apps'
INSTALLED_APPS = ['blog', 'work']

SERVER_CONFIG = {
        'host': '0.0.0.0',
        'port': '12495',
        'reloader': True
}

#-*- coding: utf-8 -*-
from bottle import default_app

from share.bottle import Avalon


# push the app into the stack FIRST!
app = Avalon(__name__)
default_app.push(app)


from .models import *
from .views import blueprint_www

app.register_blueprint(blueprint_www, url_prefix='/blog')

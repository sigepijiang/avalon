#-*- coding: utf-8 -*-

from share.framework.bottle import Avalon

# push the app into the stack FIRST!
app = Avalon(__name__)

from .views import blueprint_www

app.register_blueprint(blueprint_www)

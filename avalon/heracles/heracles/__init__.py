#-*- coding: utf-8 -*-
from share.framework.bottle import Avalon


app = Avalon(__name__)


from .models import *
from .views import blueprint_www

app.register_blueprint(blueprint_www, url_prefix='/blog')

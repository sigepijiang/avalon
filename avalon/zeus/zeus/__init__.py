#-*- coding: utf-8 -*-
from share.framework.bottle import Avalon


app = Avalon(__name__)


from zeus.views import blueprint_account
from zeus.apis import bp_apis

app.register_blueprint(blueprint_account)
app.register_blueprint(bp_apis)

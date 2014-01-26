#-*- coding: utf-8 -*-
import os
from share.framework.bottle import default_app
from share.framework.bottle import MethodView, view
from share.framework.bottle import NotFound

from heracles.models import BlogModel
from ._decorators import content2html


class IndexView(MethodView):
    @view('index.html')
    def get(self):
        pass

#-*- coding: utf-8 -*-
from share.bottle import MethodView, content2html, view
from share.bottle import NotFound

from blog.models import TextModel


class TextView(MethodView):
    @view('blog.html')
    @content2html
    def get(self, blog_id):
        blog = TextModel.query().filter_by(
            id=blog_id).first()

        if not blog:
            raise NotFound('日志不存在')

        return 'hello world'


class TextRedirectView(MethodView):
    def get(self, file_name, file_type):
        pass

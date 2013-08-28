#-*- coding: utf-8 -*-
import os
from share.bottle import default_app
from share.bottle import MethodView, view
from share.bottle import NotFound

from blog.models import BlogModel
from ._decorators import content2html


class BlogView(MethodView):
    @view('blog.html')
    def get(self, blog_id):
        blog = BlogModel.query.filter_by(
            id=blog_id).first()

        if not blog:
            raise NotFound('日志不存在')

        return blog


class TextView(MethodView):
    @view('text.html')
    @content2html
    def get(self, file_name, file_type):
        app = default_app()
        app_path = app.config.app_path
        file_path = os.path.join(
            app_path, app.config.content_path, file_type,
            '%s.%s' % (file_name, file_type))
        if not os.path.exists(file_path):
            raise NotFound('日志不存在')

        return dict(
            file_name=file_name,
            file_type=file_type)

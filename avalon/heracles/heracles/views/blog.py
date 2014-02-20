#-*- coding: utf-8 -*-
import os
from share.decorators import content2html
from share.framework.bottle import default_app
from share.framework.bottle import MethodView, view
from share.framework.bottle import NotFound

from heracles.models import BlogModel


class BlogListView(MethodView):
    @view('blog.html')
    def get(self):
        return {}


class BlogView(MethodView):
    @view('blog.html')
    def get(self, blog_id):
        blog = BlogModel.query.get(blog_id)
        return dict(blog=blog)


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

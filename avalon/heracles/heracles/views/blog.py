#-*- coding: utf-8 -*-
import os
from share.utils.decorators import content2html
from share.framework.bottle import default_app
from share.framework.bottle import MethodView, view
from share.framework.bottle import NotFound
from share.framework.bottle import Pager

from heracles.models import BlogModel


class BlogIndexView(MethodView):
    pager_limit = 5

    @view('blog/index.html')
    def get(self):
        query = BlogModel.query.filter(
            BlogModel.is_visible.is_(True)
        ).order_by(BlogModel.date_created.desc())

        pager = Pager(self)
        pager.set_total_count(query.count())

        return dict(blog_list=query.all(), pager=pager)


class BlogListView(MethodView):
    @view('blog/blog.html')
    def get(self):
        return {}


class BlogView(MethodView):
    @view('blog/blog.html')
    def get(self, blog_id):
        blog = BlogModel.query.get(blog_id)
        return dict(blog=blog)


class TextView(MethodView):
    @view('blog/text.html')
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


class BlogEditView(MethodView):
    @view('blog/edit.html')
    def get(self, blog_id):
        if blog_id:
            blog = BlogModel.query.get(blog_id)
        else:
            blog = BlogModel()

        return dict(blog=blog)

    def post(self, blog_id):
        if blog_id:
            blog = BlogModel.query.get(blog_id)
        else:
            blog = BlogModel()

        return

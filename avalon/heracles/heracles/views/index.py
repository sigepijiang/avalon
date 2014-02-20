#-*- coding: utf-8 -*-
from share.framework.bottle import MethodView, view
from share.framework.bottle import Pager

from heracles.models import BlogModel


class BlogIndexView(MethodView):
    pager_limit = 5

    @view('index.html')
    def get(self):
        query = BlogModel.query.filter(
            BlogModel.is_visible.is_(True)
        ).order_by(BlogModel.date_created.desc())

        pager = Pager(self)
        pager.set_total_count(query.count())

        return dict(blog_list=query.all(), pager=pager)

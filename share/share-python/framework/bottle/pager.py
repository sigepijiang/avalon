# -*- coding: utf-8 -*-
from bottle import request

from share.errors import AvalonException
from share.framework.bottle import render_template


class Pager(object):
    def __init__(self, view, template='default_pager.html'):
        pager_limit = getattr(view, 'pager_limit', None)
        if pager_limit is None:
            raise AvalonException(
                'The view doesn\'t have pager_limit.')

        self.pager_limit = pager_limit

        self.current_page = int(request.params.get('page', '1'))
        self.template = template

    def set_total_count(self, num):
        self.total_count = num

    def context(self):
        return dict(
            pager_limit=self.pager_limit,
            total_count=self.total_count,
            current_page=self.current_page
        )

    def __call__(self):
        return render_template(self.template, **self.context())

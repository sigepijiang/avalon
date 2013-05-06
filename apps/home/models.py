#-*- coding: utf-8 -*-
from datetime import datetime

import sqlalchemy as sa

from platform_src.engines import db, TableOpt


class Blog(db.Model, TableOpt):
    __tablename__ = 'blog'

    id = sa.Column(sa.Integer(), primary_key=True)
    title = sa.Column(sa.Unicode(256))
    file_path = sa.Column(sa.Unicode(1024), nullable=False)
    file_name = sa.Column(sa.Unicode(128), nullable=False)
    is_show = sa.Column(sa.Boolean(), default=True)
    date_created = sa.Column(sa.DateTime(), default=datetime.now)

    def __init__(self, file_path, file_name, title=''):
        self.title = title
        self.file_path = file_path
        self.file_name = file_name

#-*- coding: utf-8 -*-
from datetime import datetime

import sqlalchemy as sa

from share.engines import db, TableOpt


class TextModel(db.Model, TableOpt):
    __tablename__ = 'text'

    id = sa.Column(sa.Integer(), primary_key=True)
    hashkey = sa.Column(sa.String(128), nullable=False)
    title = sa.Column(sa.Unicode(256))
    file_type = sa.Column(sa.String(32), nullable=False)
    content_type = sa.Column(sa.String(32), nullable=False)
    file_name = sa.Column(sa.Unicode(128), nullable=False)
    is_show = sa.Column(sa.Boolean(), default=True)
    date_created = sa.Column(sa.DateTime(), default=datetime.now)
    date_modified = sa.Column(sa.DateTime(), default=datetime.now)

    def __init__(self, file_path, file_name, title=''):
        self.title = title
        self.file_path = file_path
        self.file_name = file_name

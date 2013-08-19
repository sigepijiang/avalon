#-*- coding: utf-8 -*-
from datetime import datetime

import sqlalchemy as sa

from share.engines import db, TableOpt


class TextMetaModel(db.Model, TableOpt):
    __tablename__ = 'text_meta'

    id = sa.Column(sa.Integer(), primary_key=True)
    hashkey = sa.Column(
        sa.String(128), sa.ForeignKey('text.hashkey'), nullable=False)
    file_type = sa.Column(sa.String(8), nullable=False)
    file_name = sa.Column(sa.Unicode(128), nullable=False)

    text = db.relationship('TextModel', backref='text_meta')

    def __init__(self, file_path, file_name, title=''):
        self.title = title
        self.file_path = file_path
        self.file_name = file_name


class TextModel(db.Model, TableOpt):
    __tablename__ = 'text'

    hashkey = sa.Column(sa.String(128), primary_key=True)
    parent_hashkey = sa.Column(sa.String(128))
    content = sa.Column(sa.Unicode())


class BlogModel(db.Model, TableOpt):
    __tablename__ = 'blog'

    id = sa.Column(sa.Integer(), primary_key=True)
    text_id = sa.Column(sa.Integer(), sa.ForeignKey('text_meta.id'))
    title = sa.Column(sa.Unicode(128))
    summary = sa.Column(sa.Unicode(512))
    date_created = sa.Column(sa.DateTime(), default=datetime.now)
    date_modified = sa.Column(sa.DateTime(), default=datetime.now)

    text_meta = db.relationship('TextMetaModel', backref='blog')

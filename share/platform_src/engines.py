#-*- coding: utf-8 -*-
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from settings import DATABASE


CONTENT_MODEL_DICT = {}


class DataBaseOperation(object):
    pass

db = DataBaseOperation()
db.Model = declarative_base()
db.engine = create_engine(DATABASE, echo=False)
db.session = sessionmaker(bind=db.engine)()


class TableOpt(object):
    @classmethod
    def create(cls, *args, **kwargs):
        tmp = cls(*args, **kwargs)
        db.session.add(tmp)
        db.session.commit()
        return tmp

    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def query(cls):
        return db.session.query(cls)


class ContentBaseModel(object):
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

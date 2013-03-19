#-*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from settings import DATABASE


class DataBaseOperation(object):
    pass

db = DataBaseOperation()
db.Model = declarative_base()
db.engine = create_engine(DATABASE, echo=True)
db.session = sessionmaker(bind=db.engine)()


class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

class TableOpt(object):
    @classmethod
    def create(cls, *args, **kwargs):
        tmp = cls(*args, **kwargs)
        db.session.add(tmp)
        db.session.commit()
        return tmp

    def update(self):
        db.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def query(cls):
        return db.session.query(cls)


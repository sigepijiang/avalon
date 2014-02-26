#-*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from bottle import cached_property

from share import app_stack


class TableOpt(object):
    @classmethod
    def create(cls, *args, **kwargs):
        tmp = cls(*args, **kwargs)
        db.session.add(tmp)
        db.session.commit()
        return tmp

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def as_dict(self):
        return {}


class DataBaseOperation(object):
    @cached_property
    def Model(self):
        model = declarative_base()
        model.query = self.session.query_property()
        return model

    @cached_property
    def engine(self):
        app = app_stack()
        return create_engine(
            app.config.db_master, echo=app.config.enable_sql_echo)

    @cached_property
    def session(self):
        return scoped_session(sessionmaker(bind=self.engine))

    @cached_property
    def relationship(self):
        return relationship

    @cached_property
    def backref(self):
        from sqlalchemy.orm import backref
        return backref


# TODO: delete
class SqlalchemyUtil(object):
    pass


db = DataBaseOperation()
db.utils = SqlalchemyUtil()
db.TableOpt = TableOpt
db.util = SqlalchemyUtil()

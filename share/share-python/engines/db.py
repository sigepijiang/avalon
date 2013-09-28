#-*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, text
from bottle import default_app
from bottle import cached_property


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
        app = default_app()
        return create_engine(
            app.config.db_master, echo=app.config.enable_sql_echo)

    @cached_property
    def session(self):
        return scoped_session(sessionmaker(bind=self.engine))

    @cached_property
    def relationship(self):
        return relationship


class SqlalchemyUtil(object):
    def server_datetime():
        return text('NOW()')


db = DataBaseOperation()
db.utils = SqlalchemyUtil()
db.TableOpt = TableOpt

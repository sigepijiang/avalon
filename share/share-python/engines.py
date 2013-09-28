#-*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from bottle import default_app
from bottle import cached_property


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
            app.config.sa_master, echo=app.config.enable_sql_echo)

    @cached_property
    def session(self):
        return scoped_session(sessionmaker(bind=self.engine))

    @cached_property
    def relationship(self):
        return relationship


def server_datetime():
    return 'NOW()'


sa = DataBaseOperation()


class TableOpt(object):
    @classmethod
    def create(cls, *args, **kwargs):
        tmp = cls(*args, **kwargs)
        sa.session.add(tmp)
        sa.session.commit()
        return tmp

    def update(self):
        sa.session.commit()
        return self

    def delete(self):
        sa.session.delete(self)
        sa.session.commit()
        return self

    def as_dict(self):
        return {}

#-*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship
from bottle import cached_property


class DataBaseOperation(object):
    @cached_property
    def Model(self):
        model = declarative_base()
        model.query = self.session.query_property()
        return model

    @cached_property
    def engine(self):
        raise NotImplementedError()

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

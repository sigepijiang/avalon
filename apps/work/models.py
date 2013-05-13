#-*- coding: utf-8 -*-
from platform_src.engines import db, TableOpt, ContentBaseModel


class Work(db.Model, ContentBaseModel, TableOpt):
    __tablename__ = 'work'

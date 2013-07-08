#-*- coding: utf-8 -*-
from platform_src.engines import db, TableOpt, ContentBaseModel


class Blog(db.Model, ContentBaseModel, TableOpt):
    __tablename__ = 'blog'

#-*- coding: utf-8 -*-
from datetime import datetime

from bottle import cached_property
import sqlalchemy as sa

from share.engines import db


class TextModel(db.Model, db.TableOpt):
    __tablename__ = 'text'

    hashkey = sa.Column(sa.String(128), primary_key=True)
    parent_hashkey = sa.Column(
        sa.String(128), sa.ForeignKey('text.hashkey'))
    content = sa.Column(sa.Unicode())

    parent = db.relationship('TextModel', uselist=False)



class BlogModel(db.Model, db.TableOpt):
    __tablename__ = 'blog'

    id = sa.Column(sa.Integer(), primary_key=True)
    file_name = sa.Column(sa.Unicode(64))
    title = sa.Column(sa.Unicode(128))
    text_id = sa.Column(sa.String(128), sa.ForeignKey('text.hashkey'))
    summary = sa.Column(sa.Unicode(512))
    date_created = sa.Column(sa.DateTime(), default=datetime.now)
    date_modified = sa.Column(sa.DateTime(), default=datetime.now)
    category_id = sa.Column(sa.Integer(), sa.ForeignKey('category.id'))
    is_visible = sa.Column(
        sa.Boolean(), default=True, server_default='true')

    text = db.relationship('TextModel', backref='blog', uselist=False)
    tags = db.relationship(
        'TagModel',
        primaryjoin='BlogModel.id == BlogTagsModel.blog_id',
        secondary=lambda: BlogTagsModel.__table__,
        secondaryjoin='BlogTagsModel.tag == TagModel.title',
    )

    @cached_property
    def html(self):
        return self.text.content


class CategoryModel(db.Model, db.TableOpt):
    __tablename__ = 'category'

    id = sa.Column(sa.Integer(), primary_key=True)
    title = sa.Column(sa.Unicode(32), nullable=False)


class BlogTagsModel(db.Model, db.TableOpt):
    __tablename__ = 'blog_tags'

    blog_id = sa.Column(
        sa.Integer(), sa.ForeignKey('blog.id'), primary_key=True)
    tag = sa.Column(sa.Unicode(32), sa.ForeignKey('tag.title'), primary_key=True)


class TagModel(db.Model, db.TableOpt):
    __tablename__ = 'tag'

    title = sa.Column(sa.Unicode(32), primary_key=True)

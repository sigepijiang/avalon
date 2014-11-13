#-*- coding: utf-8 -*-
from datetime import datetime

import sqlalchemy as sa

from share.framework.bottle.engines import db
from share.utils.base62 import to_python
from share.utils.snowflake import get_id


class AccountModel(db.Model, db.TableOpt):
    __tablename__ = 'account'
    ukey = sa.Column(sa.CHAR(8), primary_key=True)
    nickname = sa.Column(sa.Unicode(32), nullable=False)
    status = sa.Column(
        sa.Enum(('active', 'frozen'), 'account_status_enum'),
        default='active')
    date_last_signed_in = sa.Column(
        sa.DateTime(),
        default=datetime.now(),
        server_default=sa.func.now())

    @classmethod
    def create(cls, email, password_hash, nickname):
        email = EmailModel.create(email, password_hash)
        account = AccountModel(nickname=nickname, ukey=email.ukey)
        account.email.append(email)
        db.session.add(account)
        return account


class EmailModel(db.Model, db.TableOpt):
    __tablename__ = 'email'
    ukey = sa.Column(
        sa.CHAR(8), sa.ForeignKey('account.ukey'), nullable=False)
    email = sa.Column(sa.Unicode(320), primary_key=True)
    password_hash = sa.Column(sa.CHAR(40), nullable=False)
    date_created = sa.Column(
        sa.DateTime(),
        default=datetime.now(),
        server_default=sa.func.now())

    account = db.relationship(
        'AccountModel',
        backref=db.backref('email', lazy='joined'),
        lazy='joined', uselist=False,
    )

    @classmethod
    def create(cls, email, password_hash):
        # get_id(work_id, data_centor_id)
        new_ukey = to_python(get_id(1, 1))
        email = EmailModel(
            ukey=new_ukey, email=email, password_hash=password_hash)
        return email


class AccountAliasModel(db.Model, db.TableOpt):
    __tablename__ = 'account_alias'

    id = sa.Column('id', sa.Integer(), primary_key=True)


class IPLimitModel(db.Model, db.TableOpt):
    __tablename__ = 'ip_limit'

    id = sa.Column('id', sa.Integer(), primary_key=True)


class ClientModel(db.Model, db.TableOpt):
    __tablename__ = 'client'

    id = sa.Column('id', sa.Integer(), primary_key=True)
    secret = sa.Column(sa.String(32), nullable=False)
    name = sa.Column('name', sa.Unicode(32))
    client_type = sa.Column(
        sa.Enum(('main', 'public'), 'client_type_enum'))
    domain = sa.Column(sa.String(64))
    logo = sa.Column(sa.String(56))
    date_created = sa.Column(
        sa.DateTime(),
        default=datetime.now(),
        server_default=sa.func.now()
    )

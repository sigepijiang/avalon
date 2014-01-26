#-*- coding: utf-8 -*-
from bottle import default_app
import random
import sqlalchemy as sa

from share.engines import db
from share.utils.base62 import base62_encode


class AccountModel(db.Model, db.TableOpt):
    __tablename__ = 'account'
    ukey = sa.Column(sa.CHAR(7), primary_key=True)
    nickname = sa.Column(sa.Unicode(32), nullable=False)
    status = sa.Column(
        sa.Enum(('active', 'frozen'), 'account_status_enum'),
        default='active')
    date_last_signed_in = sa.Column(
        sa.DateTime(),
        server_default=db.utils.server_datetime)


class EmailModel(db.Model, db.TableOpt):
    __tablename__ = 'email'
    ukey = sa.Column(
        sa.CHAR(7), sa.ForeignKey('account.ukey'), nullable=False)
    email = sa.Column(sa.Unicode(320), primary_key=True)
    password_hash = sa.Column(sa.CHAR(40), nullable=False)
    date_created = sa.Column(
        sa.DateTime(), server_default=db.utils.server_datetime)

    account = db.relationship(
        'AccountModel',
        backref=db.backref('email', lazy='joined'),
        lazy='joined'
    )

    @classmethod
    def create(self, email, password_hash, nickname):
        new_ukey = UkeySequenceModel.get_new_ukey()
        account = AccountModel(nickname=nickname, ukey=new_ukey)
        email = EmailModel(email=email, password_hash=password_hash)
        email.account = account
        db.session.add(email)
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
    name = sa.Column('name', sa.Unicode(32))
    client_type = sa.Column(
        sa.Enum(('main', 'public'), 'client_type_enum'))
    domain = sa.Column(sa.String(64))
    date_created = sa.Column(
        sa.DateTime(),
        server_default=db.utils.server_datetime
    )


class UkeySequenceModel(db.Model, db.TableOpt):
    __tablename__ = 'ukey_sequence'

    id = sa.Column('id', sa.Integer(), primary_key=True)
    seq = sa.Column('seq', sa.BigInteger())

    @classmethod
    def get_new_ukey(cls):
        app = default_app()
        fill_rate = app.config.fill_rate
        seq = cls.query.first()
        if not seq:
            seq = UkeySequenceModel(seq=1)
            db.session.add(seq)
            db.commit()

        while True:
            if random.randint(1, 10) > fill_rate:
                break
            seq.seq += 1

        db.session.commit()
        return base62_encode(seq.seq)

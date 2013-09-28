#-*- coding: utf-8 -*-
import sqlalchemy as sa

from share.engines import db


class AccountModel(db.Model, db.TableOpt):
    __tablename__ = 'account',
    ukey = sa.Column(sa.CHAR(7), primary_key=True)
    nickname = sa.Column(sa.Unicode(32), nullable=False)
    status = sa.Column(
        sa.Enum(('active', 'frozen'), 'account_status_enum'),
        default='active')
    date_last_signed_in = sa.Column(
        sa.DateTime(),
        server_default=db.utils.server_datetime)


class ClientModel(db.Model, db.TableOpt):
    __tablename__ = 'client',
    id = sa.Column('id', sa.Integer(), primary_key=True)
    name = sa.Column('name', sa.Unicode(32))
    client_type = sa.Column(
        sa.Enum(('main', 'public'), 'client_type_enum'))
    domain = sa.Column(sa.String(64))
    date_created = sa.Column(
        sa.DateTime(),
        server_default=db.utils.server_datetime
    )

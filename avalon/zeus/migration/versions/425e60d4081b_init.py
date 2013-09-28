"""init

Revision ID: 425e60d4081b
Revises: None
Create Date: 2013-09-25 15:46:11.654988

"""

# revision identifiers, used by Alembic.
revision = '425e60d4081b'
down_revision = None

from alembic import op
import sqlalchemy as sa

from share.engines import db


def upgrade():
    op.create_table(
        'account',
        sa.Column('ukey', sa.CHAR(7), primary_key=True),
        sa.Column('nickname', sa.Unicode(32), nullable=False),
        sa.Column(
            'status',
            sa.Enum(('active', 'frozen'), 'account_status_enum'),
            default='active'),
        sa.Column(
            'date_last_signed_in',
            sa.DateTime(),
            server_default=db.utils.server_datetime()),
    )
    op.create_table(
        'client',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.Unicode(32)),
        sa.Column(
            'client_type',
            sa.Enum(('main', 'public'), 'client_type_enum')),
        sa.Column(
            'domain',
            sa.String(64)),
        sa.Column(
            'date_created',
            sa.DateTime(),
            server_default=db.utils.server_datetime()),
    )


def downgrade():
    op.drop_table('account')
    op.drop_table('client')

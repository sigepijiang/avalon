"""init

Revision ID: 425e60d4081b
Revises: None
Create Date: 2013-09-25 15:46:11.654988

"""

# revision identifiers, used by Alembic.
revision = '425e60d4081b'
down_revision = None

from datetime import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'account',
        sa.Column('ukey', sa.CHAR(8), primary_key=True),
        sa.Column('nickname', sa.Unicode(32), nullable=False),
        sa.Column(
            'status',
            sa.Enum('active', 'frozen', name='account_status_enum'),
            default='active'),
        sa.Column(
            'date_last_signed_in',
            sa.DateTime(),
            default=datetime.now(),
            server_default=sa.func.now()),
    )

    op.create_table(
        'email',
        sa.Column(
            'ukey', sa.CHAR(8), sa.ForeignKey('account.ukey'),
            nullable=False
        ),
        sa.Column('email', sa.Unicode(320), primary_key=True),
        sa.Column(
            'password_hash', sa.CHAR(40), nullable=False),
        sa.Column(
            'date_created', sa.DateTime(),
            default=datetime.now(),
            server_default=sa.func.now()),
    )

    op.create_table(
        'client',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('secret', sa.String(32), nullable=False),
        sa.Column('name', sa.Unicode(32)),
        sa.Column(
            'client_type',
            sa.Enum('master', 'servant', name='client_type_enum')),
        sa.Column(
            'domain',
            sa.String(64)),
        sa.Column('logo', sa.String(56)),
        sa.Column(
            'date_created',
            sa.DateTime(),
            default=datetime.now(),
            server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('email')
    op.drop_table('account')
    op.drop_table('client')
    op.execute('drop type account_status_enum;')
    op.execute('drop type client_type_enum;')

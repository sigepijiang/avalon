"""insert data

Revision ID: 1e14f4804617
Revises: 425e60d4081b
Create Date: 2014-03-22 20:32:47.627908

"""

# revision identifiers, used by Alembic.
revision = '1e14f4804617'
down_revision = '425e60d4081b'

from datetime import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    table = sa.sql.table(
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
    op.bulk_insert(table, [{
        'id': 7131,
        'secret': '55df5dde98eb34acb6b0b306a0b200fa',
        'name': u'Avalon',
        'client_type': 'master',
        'domain': 'wishstone.me',
        'logo': '',
    }])


def downgrade():
    pass

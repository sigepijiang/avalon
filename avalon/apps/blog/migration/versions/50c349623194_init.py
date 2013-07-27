"""init

Revision ID: 50c349623194
Revises: None
Create Date: 2013-07-27 13:03:32.967993

"""
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '50c349623194'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'text',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('hashkey', sa.String(128), nullable=False),
        sa.Column('title', sa.Unicode(256)),
        sa.Column('file_type', sa.String(32), nullable=False),
        sa.Column('content_type', sa.String(32), nullable=False),
        sa.Column('file_name', sa.Unicode(128), nullable=False),
        sa.Column('is_show', sa.Boolean(), default=True),
        sa.Column('date_created', sa.DateTime(), default=datetime.now),
        sa.Column('date_modified', sa.DateTime(), default=datetime.now),)


def downgrade():
    op.drop_table('text')

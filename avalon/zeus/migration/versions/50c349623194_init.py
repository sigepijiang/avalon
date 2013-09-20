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
        sa.Column('hashkey', sa.String(128), primary_key=True),
        sa.Column('parent_hashkey', sa.String(128)),
        sa.Column('content', sa.Unicode()))

    op.create_table(
        'text_meta',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column(
            'hashkey', sa.String(128), sa.ForeignKey('text.hashkey')),
        sa.Column('file_type', sa.String(32), nullable=False),
        sa.Column('file_name', sa.Unicode(128), nullable=False))

    op.create_table(
        'blog',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column(
            'text_id', sa.Integer(), sa.ForeignKey('text_meta.id')),
        sa.Column('title', sa.Unicode(128)),
        sa.Column('summary', sa.String(512)),
        sa.Column('content', sa.Unicode()),
        sa.Column('date_created', sa.DateTime(), default=datetime.now),
        sa.Column('date_modified', sa.DateTime(), default=datetime.now))


def downgrade():
    op.drop_table('blog')
    op.drop_table('text_meta')
    op.drop_table('text')

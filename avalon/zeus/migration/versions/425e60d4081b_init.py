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


def upgrade():
    op.create_table(
        'account'
        sa.Column()
    )
    op.create_table(
        'client'
    )


def downgrade():
    op.drop_table('account')
    op.drop_table('client')

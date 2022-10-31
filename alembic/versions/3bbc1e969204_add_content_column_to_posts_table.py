"""add content column to posts table

Revision ID: 3bbc1e969204
Revises: 1fcb98c492d0
Create Date: 2022-10-31 00:48:13.824770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bbc1e969204'
down_revision = '1fcb98c492d0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

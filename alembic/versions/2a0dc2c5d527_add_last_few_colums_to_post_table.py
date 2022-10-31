"""add last few colums to post table

Revision ID: 2a0dc2c5d527
Revises: 64fd6f0cb2ca
Create Date: 2022-10-31 02:41:04.994219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a0dc2c5d527'
down_revision = '64fd6f0cb2ca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', 
    sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass

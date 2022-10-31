"""create posts table

Revision ID: 1fcb98c492d0
Revises: 
Create Date: 2022-10-31 00:34:24.993076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fcb98c492d0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', 
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False)
    )

    pass


def downgrade() -> None:
    op.drop_table('posts')
    
    pass

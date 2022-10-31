"""add foreign-key to post table

Revision ID: 64fd6f0cb2ca
Revises: 9bb08c58723c
Create Date: 2022-10-31 02:35:33.748982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64fd6f0cb2ca'
down_revision = '9bb08c58723c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', 
        sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', 
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass

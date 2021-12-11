"""create post table

Revision ID: c9dd1dc50b04
Revises: 
Create Date: 2021-12-09 03:20:34.185354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9dd1dc50b04'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                            sa.Column('title', sa.String(), nullable=False)            
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass

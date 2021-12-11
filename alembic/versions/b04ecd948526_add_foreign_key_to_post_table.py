"""add foreign key to post table

Revision ID: b04ecd948526
Revises: 6f3d24c05cfe
Create Date: 2021-12-09 21:57:15.821124

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = 'b04ecd948526'
down_revision = '6f3d24c05cfe'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False)),
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
    local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass

"""create user table

Revision ID: 6f3d24c05cfe
Revises: 89540e2c6fd0
Create Date: 2021-12-09 21:13:25.750343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f3d24c05cfe'
down_revision = '89540e2c6fd0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('email', sa.String(), nullable=False),
            sa.Column('password', sa.String(), nullable=False),
            sa.Column('created_At', sa.TIMESTAMP(timezone=True), 
                        server_default=sa.text('now()'), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email') 
        )            
    pass


def downgrade():
    op.drop_table('users')
    pass

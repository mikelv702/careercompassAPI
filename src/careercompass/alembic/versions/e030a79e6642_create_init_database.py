"""create init database

Revision ID: e030a79e6642
Revises: 
Create Date: 2024-08-06 20:39:03.977120

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e030a79e6642'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade():
    # Create users table
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('full_name', sa.String(), nullable=True),
                    sa.Column('email', sa.String(), nullable=True),
                    sa.Column('hashed_password', sa.String(), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )

    # Create completed_tasks table
    op.create_table('completed_tasks',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    # Drop completed_tasks table
    op.drop_table('completed_tasks')

    # Drop users table
    op.drop_table('users')

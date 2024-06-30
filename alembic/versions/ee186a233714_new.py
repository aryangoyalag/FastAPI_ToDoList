"""New

Revision ID: ee186a233714
Revises: 
Create Date: 2024-06-29 22:11:56.978588

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee186a233714'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('username', sa.String(), unique=True, nullable=False),
        sa.Column('email', sa.String(), unique=True, nullable=False),
        sa.Column('password', sa.String(), nullable=False)
    )

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('task_title', sa.String(), unique=True, nullable=False),
        sa.Column('username', sa.String(), sa.ForeignKey('users.username'))
    )


def downgrade() -> None:
    # Drop tasks table
    op.drop_table('tasks')

    # Drop users table
    op.drop_table('users')

"""Create table for warns system

Revision ID: 2bb4f02c6291
Revises: 315baeef2e1e
Create Date: 2024-10-14 11:50:55.799270+00:00

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2bb4f02c6291'
down_revision: Union[str, None] = '315baeef2e1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users_moderations',
        sa.Column('id', sa.Integer()),
        sa.Column('user_id', sa.BigInteger()),
        sa.Column('chat_id', sa.BigInteger()),
        sa.Column('warns', sa.Integer(), default=0),
        sa.ForeignKeyConstraint(['user_id'], ['users_moderations.id'], name='fk_user_id'),
        sa.UniqueConstraint('user_id', 'chat_id', name='const_user_chat_unique'),
        sa.PrimaryKeyConstraint('id', name='const_id_primary'),
        if_not_exists=True,
        schema='warns_system' 
    )


def downgrade() -> None:
    op.drop_table(
        'users_moderations', 
        if_exists=True, 
        schema='warns_system'
    )
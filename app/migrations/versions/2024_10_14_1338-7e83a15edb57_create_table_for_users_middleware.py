"""Create table for users middleware

Revision ID: 7e83a15edb57
Revises: 2bb4f02c6291
Create Date: 2024-10-14 13:38:15.476976+00:00

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7e83a15edb57'
down_revision: Union[str, None] = '2bb4f02c6291'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'welcome_users',
        sa.Column('id', sa.Integer),
        sa.Column('chat_id', sa.BigInteger),
        sa.Column('message_id', sa.BigInteger),
        sa.UniqueConstraint('chat_id', name='const_chat_id_unique'),
        sa.PrimaryKeyConstraint('id', name='const_id_primary'),
        if_not_exists=True,
        schema='users'  
    )


def downgrade() -> None:
    op.drop_table(
        'welcome_users', 
        if_exists=True, 
        schema='users'
    ) 
"""Create reasons table

Revision ID: 702d8ae5acc2
Revises: 7e83a15edb57
Create Date: 2024-10-15 16:49:27.104349+00:00

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '702d8ae5acc2'
down_revision: Union[str, None] = '7e83a15edb57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'warns_reasons',
        sa.Column('id', sa.Integer),
        sa.Column('user_id', sa.BigInteger),
        sa.Column('chat_id', sa.BigInteger),
        sa.Column('reasons', sa.String(length=255)),
        sa.PrimaryKeyConstraint('id', name='const_id_primary'),
        if_not_exists=True,
        schema='warns_system'
    )
    
    op.create_index(
        index_name='index_user_chat_common',
        table_name='warns_reasons', 
        schema='warns_system',
        columns=['user_id', 'chat_id']
    )


def downgrade() -> None:
    op.drop_table(
        table_name='warns_reasons', 
        if_exists=True, 
        schema='warns_system'
    )
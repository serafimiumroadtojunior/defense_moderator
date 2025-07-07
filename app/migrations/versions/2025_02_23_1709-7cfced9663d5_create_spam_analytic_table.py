"""Create spam analytic table

Revision ID: 7cfced9663d5
Revises: 702d8ae5acc2
Create Date: 2025-02-23 17:09:52.599753+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7cfced9663d5'
down_revision: Union[str, None] = '702d8ae5acc2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'spam_analytic',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.BigInteger),
        sa.Column('all_count', sa.Integer, default=0),
        sa.Column('unique_count', sa.Integer, default=0),
        sa.UniqueConstraint('user_id', name='const_user_unique'),
        if_not_exists=True,
        schema='analytic'
    )

def downgrade() -> None:
    op.drop_table(
        'spam_analytic', 
        if_exists=True,
        schema='analytic'
    )
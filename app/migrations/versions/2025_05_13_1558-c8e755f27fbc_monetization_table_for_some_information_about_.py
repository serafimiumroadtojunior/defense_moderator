"""Monetization table for some information about payments

Revision ID: c8e755f27fbc
Revises: 7cfced9663d5
Create Date: 2025-05-13 15:58:58.156297+00:00

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8e755f27fbc'
down_revision: Union[str, None] = '7cfced9663d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users_checks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.BigInteger()),
        sa.Column("stars_amount", sa.Integer()),
        sa.Column("check_id", sa.String()),
        sa.Column("date_donate", sa.Date(), default=datetime.now),
        if_not_exists=True,
        schema="monetization_system"
    )


def downgrade() -> None:
    op.drop_table(
        "users_checks",
        schema="monetization_system",
        if_exists=True
    )
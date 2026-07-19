"""Create schemas

Revision ID: 315baeef2e1e
Revises: 
Create Date: 2024-10-12 11:15:55.612137+00:00

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '315baeef2e1e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS warns_system")
    op.execute("CREATE SCHEMA IF NOT EXISTS users")
    op.execute("CREATE SCHEMA IF NOT EXISTS analytic")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS warns_system")
    op.execute("DROP SCHEMA IF EXISTS users")
    op.execute("DROP SCHEMA IF EXISTS analytic")
"""add maintenance cost constraint

Revision ID: 2f08eb0e311b
Revises: c34e1c65375f
Create Date: 2026-10-01 07:10:10.494758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f08eb0e311b'
down_revision: Union[str, Sequence[str], None] = 'c34e1c65375f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_check_constraint(
        "check_maintenance_cost_non_negative",
        "maintenance_records",
        "cost >= 0",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "check_maintenance_cost_non_negative",
        "maintenance_records",
        type_="check",
    )


    # ### end Alembic commands ###

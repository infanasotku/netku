"""Adding xray record table

Revision ID: e0fa9bdc69e1
Revises: c324fbce330b
Create Date: 2024-10-21 15:24:15.941468

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e0fa9bdc69e1"
down_revision: Union[str, None] = "c324fbce330b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "xray_record",
        sa.Column("uid", sa.Uuid(), nullable=True),
        sa.Column("last_update", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("xray_record")

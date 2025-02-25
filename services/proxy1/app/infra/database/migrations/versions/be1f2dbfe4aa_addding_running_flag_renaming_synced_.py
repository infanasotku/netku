"""Addding running flag/Renaming synced flag

Revision ID: be1f2dbfe4aa
Revises: 49c249663e97
Create Date: 2025-02-24 00:35:35.017428

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "be1f2dbfe4aa"
down_revision: Union[str, None] = "49c249663e97"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("proxy_info", sa.Column("synced", sa.Boolean(), nullable=False))
    op.add_column("proxy_info", sa.Column("running", sa.Boolean(), nullable=False))
    op.drop_column("proxy_info", "synced_with_xray")


def downgrade() -> None:
    op.add_column(
        "proxy_info",
        sa.Column(
            "synced_with_xray", sa.BOOLEAN(), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("proxy_info", "running")
    op.drop_column("proxy_info", "synced")

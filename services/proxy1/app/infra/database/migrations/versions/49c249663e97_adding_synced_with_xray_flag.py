"""Adding synced with xray flag

Revision ID: 49c249663e97
Revises: 0ca314631241
Create Date: 2025-02-19 14:28:04.453263

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "49c249663e97"
down_revision: Union[str, None] = "0ca314631241"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "proxy_info", sa.Column("synced_with_xray", sa.Boolean(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("proxy_info", "synced_with_xray")

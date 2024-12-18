"""Adding availability subscription

Revision ID: afef3a44a16a
Revises: e0fa9bdc69e1
Create Date: 2024-12-13 15:33:09.881561

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "afef3a44a16a"
down_revision: Union[str, None] = "e0fa9bdc69e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("availability_subscription", sa.Boolean(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("users", "availability_subscription")
"""Adding key to proxy info/Returning old table name

Revision ID: 6e37133a80a9
Revises: ae688b85ea1a
Create Date: 2025-02-28 10:13:19.784408

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "6e37133a80a9"
down_revision: Union[str, None] = "ae688b85ea1a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "proxy_info",
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("uuid", sa.Uuid(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("addr", sa.String(), nullable=False),
        sa.Column("running", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_proxy_info_key"), "proxy_info", ["key"], unique=False)
    op.drop_table("proxy_infos")


def downgrade() -> None:
    op.create_table(
        "proxy_infos",
        sa.Column("uuid", sa.UUID(), autoincrement=False, nullable=True),
        sa.Column(
            "created", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column("addr", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("running", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name="proxy_infos_pkey"),
    )
    op.drop_index(op.f("ix_proxy_info_key"), table_name="proxy_info")
    op.drop_table("proxy_info")

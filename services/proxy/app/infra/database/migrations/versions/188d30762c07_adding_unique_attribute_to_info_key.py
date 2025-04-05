"""Adding unique attribute to info key

Revision ID: 188d30762c07
Revises: 6e37133a80a9
Create Date: 2025-02-28 10:44:18.153989

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "188d30762c07"
down_revision: Union[str, None] = "6e37133a80a9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("ix_proxy_info_key", table_name="proxy_info")
    op.create_index(op.f("ix_proxy_info_key"), "proxy_info", ["key"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_proxy_info_key"), table_name="proxy_info")
    op.create_index("ix_proxy_info_key", "proxy_info", ["key"], unique=False)

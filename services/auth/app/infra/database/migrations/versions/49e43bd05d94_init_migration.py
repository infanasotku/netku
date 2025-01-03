"""Init migration

Revision ID: 49e43bd05d94
Revises:
Create Date: 2025-01-03 22:04:22.116427

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "49e43bd05d94"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "clients",
        sa.Column("client_id", sa.String(), nullable=False),
        sa.Column("hashed_client_secret", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_clients_client_id"), "clients", ["client_id"], unique=True)
    op.create_table(
        "scopes",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "client_scopes",
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("scope_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["client_id"],
            ["clients.id"],
        ),
        sa.ForeignKeyConstraint(
            ["scope_id"],
            ["scopes.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_client_scopes_client_id"), "client_scopes", ["client_id"], unique=False
    )
    op.create_index(
        op.f("ix_client_scopes_scope_id"), "client_scopes", ["scope_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_client_scopes_scope_id"), table_name="client_scopes")
    op.drop_index(op.f("ix_client_scopes_client_id"), table_name="client_scopes")
    op.drop_table("client_scopes")
    op.drop_table("scopes")
    op.drop_index(op.f("ix_clients_client_id"), table_name="clients")
    op.drop_table("clients")

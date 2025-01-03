from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from common.sql.orm import Base


class Client(Base):
    __tablename__ = "clients"

    client_id: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    hashed_client_secret: Mapped[str] = mapped_column(nullable=False)


class Scope(Base):
    __tablename__ = "scopes"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)


class ClientScope(Base):
    __tablename__ = "client_scopes"

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"), nullable=False, index=True
    )
    scope_id: Mapped[int] = mapped_column(
        ForeignKey("scopes.id"), nullable=False, index=True
    )

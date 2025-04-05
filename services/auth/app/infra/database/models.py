from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from common.sql.orm import Base


class Client(Base):
    __tablename__ = "clients"

    def __str__(self):
        return f"[Client] {self.external_client_id}"

    external_client_id: Mapped[str] = mapped_column(
        nullable=False, unique=True, index=True
    )
    hashed_client_secret: Mapped[str] = mapped_column(nullable=False)


class Scope(Base):
    __tablename__ = "scopes"

    def __str__(self):
        return f"[Scope] {self.name}"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)


class ClientScope(Base):
    __tablename__ = "client_scopes"

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"), nullable=False, index=True
    )
    client: Mapped["Client"] = relationship("Client")

    scope_id: Mapped[int] = mapped_column(
        ForeignKey("scopes.id"), nullable=False, index=True
    )
    scope: Mapped["Scope"] = relationship("Scope")

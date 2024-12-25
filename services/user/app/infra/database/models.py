from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from app.infra.database.orm import Base


class User(Base):
    __tablename__ = "users"

    phone_number: Mapped[str] = mapped_column(nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=True)

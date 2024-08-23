from db.database import Base
from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped
from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    phone_number: Mapped[str] = mapped_column(nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=True)

    # Subscriptions
    proxy_subscription: Mapped[bool] = mapped_column(default=False, nullable=False)

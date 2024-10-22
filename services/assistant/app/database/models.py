from datetime import datetime
from uuid import UUID
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    phone_number: Mapped[str] = mapped_column(nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=True)

    # Subscriptions
    proxy_subscription: Mapped[bool] = mapped_column(default=False, nullable=False)

    booking_accounts: Mapped[list["BookingAccount"]] = relationship(
        "BookingAccount", cascade="all,delete", back_populates="owner"
    )


class BookingAccount(Base):
    __tablename__ = "booking_accounts"

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(unique=False, nullable=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="booking_accounts")


class XrayRecord(Base):
    __tablename__ = "xray_record"

    uid: Mapped[UUID] = mapped_column(nullable=True)
    last_update: Mapped[datetime] = mapped_column(nullable=False)

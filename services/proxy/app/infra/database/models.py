from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import mapped_column, Mapped

from common.sql.orm import Base


class ProxyInfo(Base):
    __tablename__ = "proxy_info"

    key: Mapped[str] = mapped_column(nullable=False, index=True)

    uuid: Mapped[UUID] = mapped_column(nullable=True)
    created: Mapped[datetime] = mapped_column(nullable=False)
    addr: Mapped[str] = mapped_column(nullable=False)
    running: Mapped[bool] = mapped_column(nullable=False, default=False)

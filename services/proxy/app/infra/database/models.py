from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import mapped_column, Mapped

from common.sql.orm import Base


class ProxyInfo(Base):
    __tablename__ = "proxy_info"

    uuid: Mapped[UUID] = mapped_column(nullable=True)
    last_update: Mapped[datetime] = mapped_column(nullable=False)

    synced_with_xray: Mapped[bool] = mapped_column(nullable=False, default=False)

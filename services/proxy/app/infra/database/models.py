from datetime import datetime
from sqlalchemy import UUID
from sqlalchemy.orm import mapped_column, Mapped

from common.sql.orm import Base


class ProxyInfo(Base):
    __tablename__ = "proxy_info"

    uuid: Mapped[UUID] = mapped_column(nullable=True)
    last_update: Mapped[datetime] = mapped_column(nullable=False)

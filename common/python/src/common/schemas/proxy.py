from datetime import datetime
from uuid import UUID

from pydantic import Field

from common.schemas import BaseSchemaPK


class ProxyInfoSchema(BaseSchemaPK):
    running: bool = Field(default=False)
    created: datetime
    uuid: UUID | None = None
    addr: str
    key: str

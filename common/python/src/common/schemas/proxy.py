from datetime import datetime
from uuid import UUID

from pydantic import Field

from common.schemas import BaseSchema


class ProxyInfoSchema(BaseSchema):
    running: bool = Field(default=False)
    created: datetime
    uuid: UUID
    addr: str

from datetime import datetime
from common.schemas import BaseSchema


class TokenPayload(BaseSchema):
    client_id: str
    scopes: list[str]
    expire: datetime

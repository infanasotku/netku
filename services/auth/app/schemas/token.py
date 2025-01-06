from datetime import datetime
from pydantic import ConfigDict
from common.schemas import BaseSchema


class TokenPayload(BaseSchema):
    client_id: str
    scopes: list[str]
    expire: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "client_id": "Test",
                    "scopes": "users:read users:write",
                    "expire": datetime.now(),
                }
            ]
        },
    )


class TokenSchema(BaseSchema):
    access_token: str
    token_type: str

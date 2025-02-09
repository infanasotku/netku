from datetime import datetime
from pydantic import ConfigDict
from common.schemas import BaseSchema
from common.schemas.token import TokenPayload


class TokenPayload(TokenPayload):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "external_client_id": "johndoe",
                    "scopes": "users:read users:write",
                    "expire": datetime.now(),
                },
            ]
        },
    )


class TokenSchema(BaseSchema):
    access_token: str
    token_type: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "access_token": "jwt.token.example",
                    "token_type": "Bearer",
                }
            ]
        },
    )

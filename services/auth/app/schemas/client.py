from common.schemas import BaseSchema, BaseSchemaPK


class ClientUpdateSchema(BaseSchema):
    external_client_id: str | None = None
    hashed_client_secret: str | None = None


class ClientCreateSchema(BaseSchemaPK):
    external_client_id: str
    hashed_client_secret: str


class ClientSchema(ClientCreateSchema):
    pass


class ClientFullSchema(ClientSchema):
    scopes: list[str]

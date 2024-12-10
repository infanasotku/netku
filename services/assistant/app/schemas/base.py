from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseSchemaPK(BaseSchema):
    id: int | str | None = None

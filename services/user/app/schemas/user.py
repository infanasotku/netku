from app.schemas.base import BaseSchema, BaseSchemaPK


class UserUpdateSchema(BaseSchema):
    phone_number: str | None = None
    telegram_id: int | None = None


class UserCreateSchema(BaseSchemaPK):
    phone_number: str | None
    telegram_id: int | None


class UserSchema(UserCreateSchema):
    pass

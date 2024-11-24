from app.schemas.base import BaseSchemaPK


class BookingAccountCreateSchema(BaseSchemaPK):
    email: str
    password: str
    owner_id: int


class BookingAccountSchema(BookingAccountCreateSchema):
    pass

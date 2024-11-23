from app.schemas.base_schema import BaseSchemaPK


class BookingAccountCreateSchema(BaseSchemaPK):
    email: str
    password: str
    owner_id: int


class BookingAccountSchema(BookingAccountCreateSchema):
    pass

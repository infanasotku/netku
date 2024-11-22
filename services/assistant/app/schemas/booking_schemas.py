from app.schemas.base_schema import BaseSchemaPK


class BookingAccountCreateSchema(BaseSchemaPK):
    email: str
    password: str


class BookingAccountSchema(BookingAccountCreateSchema):
    pass

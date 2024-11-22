from app.schemas.base_schema import BaseSchema


class BookingAccountCreateSchema(BaseSchema):
    email: str
    password: str


class BookingAccountSchema(BookingAccountCreateSchema):
    pass

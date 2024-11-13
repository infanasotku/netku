from app.schemas.schema import BaseSchema


class BookingAccountSchema(BaseSchema):
    email: str
    password: str

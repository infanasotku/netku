from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BookingRequest(_message.Message):
    __slots__ = ("email", "password")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    def __init__(
        self, email: _Optional[str] = ..., password: _Optional[str] = ...
    ) -> None: ...

class BookingResponse(_message.Message):
    __slots__ = ("booked",)
    BOOKED_FIELD_NUMBER: _ClassVar[int]
    booked: bool
    def __init__(self, booked: bool = ...) -> None: ...

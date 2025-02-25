from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class XrayInfo(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class XrayFullInfo(_message.Message):
    __slots__ = ("uuid", "running")
    UUID_FIELD_NUMBER: _ClassVar[int]
    RUNNING_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    running: bool
    def __init__(self, uuid: _Optional[str] = ..., running: bool = ...) -> None: ...

class Null(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

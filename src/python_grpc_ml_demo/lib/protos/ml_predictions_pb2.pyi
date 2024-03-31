from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Image(_message.Message):
    __slots__ = ("mode", "width", "height", "data")
    MODE_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    mode: str
    width: int
    height: int
    data: bytes
    def __init__(self, mode: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...

class Prediction(_message.Message):
    __slots__ = ("prediction",)
    PREDICTION_FIELD_NUMBER: _ClassVar[int]
    prediction: str
    def __init__(self, prediction: _Optional[str] = ...) -> None: ...

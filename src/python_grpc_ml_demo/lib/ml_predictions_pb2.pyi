from typing import (
    ClassVar as _ClassVar,
)
from typing import (
    Iterable as _Iterable,
)
from typing import (
    Mapping as _Mapping,
)
from typing import (
    Optional as _Optional,
)
from typing import (
    Union as _Union,
)

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class Image(_message.Message):
    __slots__ = ("mode", "width", "height", "data", "frame")
    MODE_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    FRAME_FIELD_NUMBER: _ClassVar[int]
    mode: str
    width: int
    height: int
    data: bytes
    frame: int
    def __init__(
        self,
        mode: _Optional[str] = ...,
        width: _Optional[int] = ...,
        height: _Optional[int] = ...,
        data: _Optional[bytes] = ...,
        frame: _Optional[int] = ...,
    ) -> None: ...

class Prediction(_message.Message):
    __slots__ = ("xmin", "ymin", "xmax", "ymax", "name")
    XMIN_FIELD_NUMBER: _ClassVar[int]
    YMIN_FIELD_NUMBER: _ClassVar[int]
    XMAX_FIELD_NUMBER: _ClassVar[int]
    YMAX_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    xmin: float
    ymin: float
    xmax: float
    ymax: float
    name: str
    def __init__(
        self,
        xmin: _Optional[float] = ...,
        ymin: _Optional[float] = ...,
        xmax: _Optional[float] = ...,
        ymax: _Optional[float] = ...,
        name: _Optional[str] = ...,
    ) -> None: ...

class PredictionCollection(_message.Message):
    __slots__ = ("object", "frame")
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    FRAME_FIELD_NUMBER: _ClassVar[int]
    object: _containers.RepeatedCompositeFieldContainer[Prediction]
    frame: int
    def __init__(
        self, object: _Optional[_Iterable[_Union[Prediction, _Mapping]]] = ..., frame: _Optional[int] = ...
    ) -> None: ...

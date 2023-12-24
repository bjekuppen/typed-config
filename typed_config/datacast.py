from enum import Enum
from typing import Any, Callable, Type

def enum(enum:Type[Enum]) -> Callable[[Any], Any]:
    def _datacast_enum(data:Any) -> Enum:
        return enum(data)
    return _datacast_enum
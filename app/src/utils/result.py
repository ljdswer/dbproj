from dataclasses import dataclass
from typing import Union, Dict, TypeVar, Generic

T = TypeVar('T')
@dataclass
class Result(Generic[T]):
    value: Union[T, None] = None
    error: str = ""

    def is_err(self):
        return bool(self.error)

    def is_ok(self):
        return not self.is_err()
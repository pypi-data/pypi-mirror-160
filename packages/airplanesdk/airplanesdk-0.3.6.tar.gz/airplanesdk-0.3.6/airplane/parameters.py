

from dataclasses import dataclass
from typing import Optional, TypeVar


T = TypeVar('T')

@dataclass
class Parameter:
    type: str
    name: Optional[str] = None
    description: Optional[str] = None
    required: Optional[bool] = None
    default: Optional[T] = None
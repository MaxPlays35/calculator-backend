from dataclasses import dataclass

from .consts import Type


@dataclass
class Function:
    value: str
    type = Type.FUNCTION

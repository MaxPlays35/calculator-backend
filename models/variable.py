from dataclasses import dataclass

from .consts import Type


@dataclass
class Variable:
    value: str
    type = Type.VARIABLE

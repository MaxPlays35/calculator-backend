from dataclasses import dataclass
from .consts import Type


@dataclass
class LeftBracket:
    value: str
    type = Type.LEFT_BRACKET


@dataclass
class RightBracket:
    value: str
    type = Type.RIGHT_BRACKET

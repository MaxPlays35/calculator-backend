from typing import Union
from dataclasses import dataclass

from .consts import Type


@dataclass
class Number:
    value: Union[int, float]
    type = Type.NUMBER

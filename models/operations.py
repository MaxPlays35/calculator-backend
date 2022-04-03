from dataclasses import dataclass

from .consts import Type, Operators, Priority

mapping = {
    "+": Operators.PLUS,
    "-": Operators.MINUS,
    "*": Operators.MULTIPLY,
    "/": Operators.DIVIDE,
    "^": Operators.EXPONENTIATION,
}

priorities = {
    "+": Priority.PLUS,
    "-": Priority.MINUS,
    "*": Priority.MULTIPLY,
    "/": Priority.DIVIDE,
    "^": Priority.EXPONENTIATION,
}


@dataclass
class Operator:
    value: str
    operator: str = None
    type = Type.OPERATOR
    operator = None
    priority = None

    def __post_init__(self):
        self.priority = priorities[self.value]
        self.operator = mapping[self.value]

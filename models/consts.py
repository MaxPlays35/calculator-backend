from enum import Enum

EPSILON = 0.0000001
STEPS = 500_000


class Type(Enum):
    OPERATOR = 0
    NUMBER = 1
    FUNCTION = 2
    LEFT_BRACKET = 3
    RIGHT_BRACKET = 4
    VARIABLE = 5


class Operators(Enum):
    PLUS = 0
    MINUS = 1
    MULTIPLY = 2
    DIVIDE = 3
    EXPONENTIATION = 4


class Priority(Enum):
    PLUS = 1
    MINUS = 1
    DIVIDE = 2
    MULTIPLY = 2
    EXPONENTIATION = 3


# class Type(Enum):
#     INTEGER = 0
#     FLOAT = 1

from math import cos, exp, log, log10, sin, tan
from collections import deque
from typing import List, Union
import models
from models import Type, Operators, Number

funcs = {
    "sin": sin,
    "cos": cos,
    "tg": tan,
    "ctg": lambda value: 1 / tan(value),
    "lg": log10,
    "ln": log,
    "exp": exp,
}
# add negative versions
funcs.update({f"-{k}": lambda val: -v(val) for k, v in funcs.items()})


def calculate(
    polish_record: List[
        Union[
            models.LeftBracket,
            models.RightBracket,
            models.Operator,
            models.Number,
            models.Variable,
            models.Function,
        ]
    ],
    x: Union[int, float] = None,
):
    stack = deque()

    for token in polish_record:
        if token.type == Type.FUNCTION:
            arg = stack.pop()
            result = funcs[token.value](arg.value)
            stack.append(Number(result))
            continue
        if token.type == Type.OPERATOR:
            if token.operator == Operators.PLUS:
                a = stack.pop().value
                b = stack.pop().value
                stack.append(Number(a + b))
            elif token.operator == Operators.MINUS:
                a = stack.pop().value
                b = stack.pop().value
                stack.append(Number(b - a))
            elif token.operator == Operators.MULTIPLY:
                a = stack.pop().value
                b = stack.pop().value
                stack.append(Number(b * a))
            elif token.operator == Operators.DIVIDE:
                a = stack.pop().value
                b = stack.pop().value
                stack.append(Number(b / a))
            elif token.operator == Operators.EXPONENTIATION:
                a = stack.pop().value
                b = stack.pop().value
                stack.append(Number(b**a))
            continue
        if token.type == Type.NUMBER:
            stack.append(token)
            continue
        if token.type == Type.VARIABLE:
            if x:
                stack.append(x)
                continue

    return stack.pop().value

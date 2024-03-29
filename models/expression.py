from copy import copy
from decimal import DivisionByZero
from typing import List, Union
from helpers import Lexer
from .brackets import RightBracket, LeftBracket
from .consts import Operators, Type, EPSILON, STEPS
from .number import Number
from .function import Function
from .operations import Operator
from .variable import Variable
from collections import deque
from queue import Queue
from math import cos, exp, log, log10, sin, tan


pos_funcs = {
    "sin": sin,
    "cos": cos,
    "tg": tan,
    "ctg": lambda value: 1 / tan(value),
    "lg": log10,
    "ln": log,
    "exp": exp,
}

funcs = copy(pos_funcs)
# add negative versions
# funcs.update({f"-{k}": lambda _: print(v) for k, v in funcs.items()})
for fn, n in pos_funcs.items():
    funcs[f"-{fn}"] = lambda value: -1 * n(value)
print(funcs.items())
print(funcs["-cos"](3.14))


class Expression:
    def __init__(self, expr) -> None:
        self.lexer = Lexer()
        self.expr = expr

    def translate(
        self,
    ) -> List[Union[LeftBracket, RightBracket, Operator, Number, Variable, Function]]:
        stack = deque()
        queue = Queue()

        for token in self.parsed:
            if token.type in [Type.NUMBER, Type.VARIABLE]:
                queue.put(token)
                continue

            if token.type == Type.OPERATOR:
                if not stack or stack[-1].type == Type.LEFT_BRACKET:
                    stack.append(token)
                    continue
                if stack[-1].type == Type.OPERATOR:
                    if stack[-1].priority.value < token.priority.value:
                        stack.append(token)
                        continue
                    if stack[-1].priority.value >= token.priority.value:
                        while (
                            stack
                            and stack[-1].type != Type.LEFT_BRACKET
                            and token.priority.value <= stack[-1].priority.value
                        ):
                            queue.put(stack.pop())

                        stack.append(token)
                        continue
            if token.type == Type.FUNCTION:
                stack.append(token)
                continue

            if token.type == Type.LEFT_BRACKET:
                stack.append(token)
                continue

            if token.type == Type.RIGHT_BRACKET:
                while stack and stack[-1].type != Type.LEFT_BRACKET:
                    queue.put(stack.pop())
                if stack:
                    stack.pop()
                if stack and stack[-1].type != Type.OPERATOR:
                    queue.put(stack.pop())
        for _ in range(len(stack)):
            queue.put(stack.pop())

        self.translated = queue.queue
        return queue.queue

    def parse(self):
        parsed, error, pos = self.lexer.parse(self.expr)
        self.parsed = parsed
        return parsed, error, pos

    def calculate(self, x: Number = None):
        try:
            stack = deque()

            for token in self.translated:
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
        except DivisionByZero:
            return None

    def find_root(self, a: Union[int, float], b: Union[int, float]):
        # step = 1
        # a = min(a, b)
        # b = max(a, b)

        # while 1:
        #     a1 = self.calculate(Number(a))
        #     b1 = self.calculate(Number(b))

        #     if a1 == b1 or a1 is None or b1 is None:
        #         return None

        #     x = a - (b - a) * a1 / (b1 - a1)

        #     a = b
        #     b = x

        #     print(step, x)

        #     value = self.calculate(Number(x))
        #     if value is None:
        #         return None

        #     if abs(value) <= EPSILON:
        #         break

        #     if step >= STEPS:
        #         return None

        #     step += 1

        # return x
        # x = b - (
        #     self.calculate(Number(b))
        #     / (self.calculate(Number(b)) - self.calculate(Number(a))
        # ) * (b - a)
        # x = b - (
        #     self.calculate(Number(b))
        #     / (self.calculate(Number(b)) - self.calculate(Number(a)))
        # ) * (b - a)

        # while abs(self.calculate(Number(x))) > EPSILON:
        #     print(x)
        #     x = b - (
        #         self.calculate(Number(b))
        #         / (self.calculate(Number(b)) - self.calculate(Number(a)))
        #     ) * (b - a)
        #     if abs(a - x) < abs(b - x):
        #         a = x
        #     else:
        #         b = x
        x = a
        # print((self.calculate(Number(a)) * self.calculate(Number(b))) > 0)
        if (self.calculate(Number(a)) * self.calculate(Number(b))) > 0:
            return None
        else:
            while (
                self.calculate(Number(a)) * self.calculate(Number(b)) < 0
                and abs(self.calculate(Number(x))) > EPSILON
            ):
                k = (self.calculate(Number(a)) - self.calculate(Number(b))) / (a - b)
                b = self.calculate(Number(a)) - k * a
                x = -b / k
                if (self.calculate(Number(x)) * self.calculate(Number(a))) > 0:
                    a = x
                else:
                    b = x
            return x

    def simpson(self, a: Union[int, float], b: Union[int, float]):
        dx = (b - a) / STEPS
        s = 0
        for step in range(0, STEPS):
            s += (dx / 6) * (
                self.calculate(Number(a + dx * step))
                + 4
                * self.calculate(Number(((a + dx * step) + (a + dx * (step + 1))) / 2))
                + self.calculate(Number(a + dx * (step + 1)))
            )

        return s

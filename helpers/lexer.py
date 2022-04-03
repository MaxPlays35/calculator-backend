import string
from typing import List, Union
import models

signs: str = "+-*/^"


class Lexer:
    def __init__(self) -> None:
        self.buffer = ""
        self.current_state = "S"
        self.machine = {
            "S": self.s_func,
            "I": self.i_func,
            "R": self.r_func,
            "B": self.b_func,
            "F": self.f_func,
            "X": self.x_func,
        }
        self.counter = 0
        self.lexsems = []

    def s_func(self, char: str):
        if char in string.digits:
            self.buffer += char

            return "I", False

        if char == "(":
            self.lexsems.append(models.LeftBracket(char))
            self.counter += 1

            return "S", False

        if char == "-":
            self.buffer += char

            return "S", False

        if char != "x" and char in string.ascii_lowercase:
            self.buffer += char

            return "F", False

        if char == "x":
            self.buffer += char

            return "X", False

    def i_func(self, char: str):
        if char in string.digits:
            self.buffer += char

            return "I", False

        if char == ".":
            self.buffer += char

            return "R", False

        if char in signs:
            self.lexsems.append(models.Number(int(self.buffer)))
            self.lexsems.append(models.Operator(char))

            return "S", True

        if char == ")":
            self.lexsems.append(models.Number(int(self.buffer)))
            self.lexsems.append(models.RightBracket(char))
            if self.counter < 0:
                return
            self.counter -= 1
            return "B", True

        if char in string.ascii_lowercase and char != "x":
            self.buffer += char

            return "F", False

    def r_func(self, char: str):
        if char in string.digits:
            self.buffer += char

            return "R", False

        if char in signs:
            self.lexsems.append(models.Number(float(self.buffer)))
            self.lexsems.append(models.Operator(char))

            return "S", True

        if char == ")":
            if self.counter < 0:
                return
            self.counter -= 1
            self.lexsems.append(models.Number(float(self.buffer)))
            self.lexsems.append(models.RightBracket(char))

            return "B", True

    def b_func(self, char: str):
        if char == ")":
            self.lexsems.append(models.RightBracket(char))
            if self.counter < 0:
                return
            self.counter -= 1

            return "B", False

        if char in signs:
            self.lexsems.append(models.Operator(char))

            return "S", False

    def f_func(self, char: str):
        if char in string.ascii_lowercase:
            self.buffer += char

            return "F", False

        if char == "(":
            self.counter += 1
            self.lexsems.append(models.Function(self.buffer))
            self.lexsems.append(models.LeftBracket(char))

            return "S", True

    def x_func(self, char: str):
        if char in signs:
            self.lexsems.append(models.Variable(self.buffer))
            self.lexsems.append(models.Operator(char))

            return "S", True

        if char == ")":
            if self.counter < 0:
                return
            self.counter -= 1
            self.lexsems.append(models.Variable(self.buffer))
            self.lexsems.append(models.RightBracket(char))
            return "B", True

    def parse(
        self, expression: str
    ) -> List[
        Union[
            models.LeftBracket,
            models.RightBracket,
            models.Operator,
            models.Number,
            models.Variable,
            models.Function,
        ]
    ]:
        for index, char in enumerate(expression):
            result = self.machine[self.current_state](char)

            if not result:
                self.lexsems = []
                return [], True, index

            self.current_state = result[0]

            if result[1]:
                self.buffer = ""

        if self.buffer:
            if self.current_state == "I":
                self.lexsems.append(models.Number(int(self.buffer)))
            elif self.current_state == "R":
                self.lexsems.append(models.Number(float(self.buffer)))
            elif self.buffer == "x":
                self.lexsems.append(models.Variable(self.buffer))
            # else:
            #     self.lexsems.append(self.buffer)

        if self.current_state not in ["S", "I", "R", "X", "B"] or self.counter != 0:
            self.lexsems = []
            return [], True, index

        return self.lexsems, False, 0

    def clear(self):
        self.buffer = ""
        self.lexsems = []
        self.current_state = "S"

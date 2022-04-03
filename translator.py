from typing import Union, List

# from helpers import Lexer
from collections import deque
from queue import Queue
from models import Type
import models


def translate(
    parsed: List[
        Union[
            models.LeftBracket,
            models.RightBracket,
            models.Operator,
            models.Number,
            models.Variable,
            models.Function,
        ]
    ]
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
    stack = deque()
    queue = Queue()

    for token in parsed:
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
                    while True:
                        if not stack or stack[-1].type == Type.LEFT_BRACKET:
                            break
                        if token.priority.value <= stack[-1].priority.value:
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
            while stack[-1].type != Type.LEFT_BRACKET:
                queue.put(stack.pop())
            stack.pop()
            if stack and stack[-1].type != Type.OPERATOR:
                queue.put(stack.pop())
    for _ in range(len(stack)):
        queue.put(stack.pop())

    return queue.queue

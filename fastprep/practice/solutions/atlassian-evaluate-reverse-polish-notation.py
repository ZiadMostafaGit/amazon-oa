# Stack evaluation of postfix tokens with division truncating toward zero.
from typing import List, Optional, Any


def evalRPN(tokens: List[str]) -> int:
    stack: List[int] = []
    for token in tokens:
        if token in ("+", "-", "*", "/"):
            right = stack.pop()
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            else:
                quotient = abs(left) // abs(right)
                if (left < 0) != (right < 0):
                    quotient = -quotient
                stack.append(quotient)
        else:
            stack.append(int(token))
    return stack[-1]

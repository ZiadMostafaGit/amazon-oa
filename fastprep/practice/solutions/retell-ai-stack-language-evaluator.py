# Straight stack-machine interpretation of the whitespace-separated token stream.
from typing import List, Optional, Any


def _is_int_token(tok: str) -> bool:
    body = tok[1:] if tok[0] == '-' else tok
    return len(body) > 0 and body.isdigit()


def _trunc_div(a: int, b: int) -> int:
    q = abs(a) // abs(b)
    if (a < 0) != (b < 0):
        q = -q
    return q


def evaluateStackProgram(program: str) -> List[int]:
    if not program:
        return []
    stack: List[int] = []
    out: List[int] = []
    for tok in program.split():
        if _is_int_token(tok):
            stack.append(int(tok))
        elif tok == '.':
            out.append(stack.pop())
        elif tok == 'dup':
            stack.append(stack[-1])
        elif tok == 'swap':
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif tok == 'pop' or tok == 'drop':
            stack.pop()
        else:
            right = stack.pop()
            left = stack.pop()
            if tok == '+':
                stack.append(left + right)
            elif tok == '-':
                stack.append(left - right)
            elif tok == '*':
                stack.append(left * right)
            else:
                stack.append(_trunc_div(left, right))
    return out

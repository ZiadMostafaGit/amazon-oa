# Tokenize on whitespace and simulate the stack until the terminating X.
from typing import List, Optional, Any


def stackOutput(commands: str) -> List[int]:
    tokens = commands.split()
    stack: List[int] = []
    out: List[int] = []
    i = 0
    n = len(tokens)
    while i < n:
        t = tokens[i]
        if t == 'X':
            break
        if t == 'U':
            stack.append(int(tokens[i + 1]))
            i += 2
            continue
        if t == 'O':
            if stack:
                out.append(stack.pop())
            i += 1
            continue
        i += 1
    return out

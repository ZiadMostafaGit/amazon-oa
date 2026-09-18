# Explicit stack of parent keys; emit each leaf prefixed by the current path.
from typing import List, Optional, Any


def flattenNestedMap(tokens: List[str]) -> List[str]:
    stack: List[str] = []
    out: List[str] = []
    for token in tokens:
        if token == "}":
            if stack:
                stack.pop()
        elif token.endswith("{"):
            stack.append(token[:-1])
        else:
            if stack:
                out.append(".".join(stack) + "." + token)
            else:
                out.append(token)
    return out

# Stack-based recursive-descent parse of the token stream into nested lists, then str().
from typing import List, Optional, Any


def readRichText(tokens: List[str]) -> str:
    root: List[Any] = []
    stack: List[List[Any]] = [root]
    for tok in tokens:
        if tok == "(":
            new: List[Any] = []
            stack[-1].append(new)
            stack.append(new)
        elif tok == ")":
            if len(stack) > 1:
                stack.pop()
        else:
            stack[-1].append(tok)
    return str(root)

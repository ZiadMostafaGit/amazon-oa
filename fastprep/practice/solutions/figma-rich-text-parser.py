# Approach: stack of open groups; each depth rise pushes new groups, each fall pops them.
from typing import List, Optional, Any


def readRichText(tokens: List[str]) -> str:
    root: List[Any] = []
    stack: List[List[Any]] = [root]  # stack[0] is the document; depth == len(stack) - 1
    for i in range(0, len(tokens) - 1, 2):
        depth = int(tokens[i])
        word = tokens[i + 1]
        while len(stack) - 1 < depth:
            new_group: List[Any] = []
            stack[-1].append(new_group)
            stack.append(new_group)
        while len(stack) - 1 > depth:
            stack.pop()
        stack[-1].append(word)
    return str(root)

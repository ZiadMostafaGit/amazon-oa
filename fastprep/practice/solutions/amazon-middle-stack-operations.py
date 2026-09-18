# Plain list as the stack: top is the last element, lower middle sits at index (n-1)//2, all O(1).
from typing import List, Optional, Any


def solve(operations: List[List[str]]) -> List[str]:
    stack = []
    out = []
    for op in operations:
        name = op[0]
        if name == "push":
            stack.append(op[1])
        elif name == "pop":
            out.append(stack.pop() if stack else "EMPTY")
        elif name == "top":
            out.append(stack[-1] if stack else "EMPTY")
        elif name == "middle":
            out.append(stack[(len(stack) - 1) // 2] if stack else "EMPTY")
    return out

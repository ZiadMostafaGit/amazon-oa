from typing import List, Optional, Any


def preorderTraversal(tree: List[int]) -> List[int]:
    n = len(tree)
    out = []
    stack = [0] if n and tree[0] != -1 else []
    while stack:
        i = stack.pop()
        out.append(tree[i])
        for c in (2 * i + 2, 2 * i + 1):
            if c < n and tree[c] != -1:
                stack.append(c)
    return out

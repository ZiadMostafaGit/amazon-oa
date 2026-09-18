# Build child lists, then iterative DFS from deleteIndex marking the subtree as -1.
from typing import List, Optional, Any


def markDeletedSubtree(parent: List[int], deleteIndex: int) -> List[int]:
    n = len(parent)
    children = [[] for _ in range(n)]
    for i, p in enumerate(parent):
        if p != i:
            children[p].append(i)
    result = list(parent)
    stack = [deleteIndex]
    result[deleteIndex] = -1
    while stack:
        node = stack.pop()
        for ch in children[node]:
            if result[ch] != -1:
                result[ch] = -1
                stack.append(ch)
    return result

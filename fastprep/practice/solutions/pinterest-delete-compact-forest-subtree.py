# Build child lists, iterative BFS to mark the deleted subtree, then prefix-count remap.
from typing import List, Optional, Any


def deleteAndCompactSubtree(parent: List[int], deleteIndex: int) -> List[int]:
    n = len(parent)
    children = [[] for _ in range(n)]
    for i, p in enumerate(parent):
        if p != i:
            children[p].append(i)
    removed = [False] * n
    stack = [deleteIndex]
    removed[deleteIndex] = True
    while stack:
        node = stack.pop()
        for ch in children[node]:
            if not removed[ch]:
                removed[ch] = True
                stack.append(ch)
    newIndex = [-1] * n
    nxt = 0
    for i in range(n):
        if not removed[i]:
            newIndex[i] = nxt
            nxt += 1
    result = []
    for i in range(n):
        if not removed[i]:
            result.append(newIndex[parent[i]])
    return result

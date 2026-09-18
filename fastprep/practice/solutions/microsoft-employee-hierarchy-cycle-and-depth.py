# Build child lists, BFS from the root; any unreachable node means a cycle in the functional graph.
from typing import List, Optional, Any
from collections import deque


def analyzeHierarchy(manager: List[int]) -> List[int]:
    n = len(manager)
    children = [[] for _ in range(n)]
    root = -1
    for i, m in enumerate(manager):
        if m == -1:
            root = i
        else:
            children[m].append(i)
    q = deque([root])
    seen = 1
    depth = 0
    while q:
        for _ in range(len(q)):
            u = q.popleft()
            for v in children[u]:
                seen += 1
                q.append(v)
        if q:
            depth += 1
    if seen != n:
        return [1, -1]
    return [0, depth]

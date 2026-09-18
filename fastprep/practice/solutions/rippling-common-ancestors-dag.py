# Reverse-graph BFS from each target, then intersect the two ancestor sets.
from typing import List, Optional, Any
from collections import deque


def commonAncestors(nodeCount: int, parentEdges: List[List[int]], first: int, second: int) -> List[int]:
    parents = [[] for _ in range(nodeCount)]
    for parent, child in parentEdges:
        parents[child].append(parent)

    def ancestors(start: int) -> bytearray:
        seen = bytearray(nodeCount)
        queue = deque()
        for p in parents[start]:
            if not seen[p]:
                seen[p] = 1
                queue.append(p)
        while queue:
            node = queue.popleft()
            for p in parents[node]:
                if not seen[p]:
                    seen[p] = 1
                    queue.append(p)
        return seen

    a = ancestors(first)
    b = ancestors(second)
    return [i for i in range(nodeCount) if a[i] and b[i]]

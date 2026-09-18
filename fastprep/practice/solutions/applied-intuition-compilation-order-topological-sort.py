# Kahn topological sort with a min-heap for the lexicographically smallest available module.
import heapq
from typing import List, Optional, Any


def compilationOrder(modules: List[str], dependencies: List[List[str]]) -> List[str]:
    adj = {m: [] for m in modules}
    indeg = {m: 0 for m in modules}

    seen = set()
    for pair in dependencies:
        a, b = pair[0], pair[1]  # a depends on b -> edge b -> a
        if (a, b) in seen:
            continue
        seen.add((a, b))
        if b not in adj:
            adj[b] = []
            indeg[b] = 0
        if a not in adj:
            adj[a] = []
            indeg[a] = 0
        adj[b].append(a)
        indeg[a] += 1

    heap = [m for m in indeg if indeg[m] == 0]
    heapq.heapify(heap)

    order = []
    while heap:
        m = heapq.heappop(heap)
        order.append(m)
        for nxt in adj[m]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)

    if len(order) != len(indeg):
        return ["IMPOSSIBLE"]
    return order

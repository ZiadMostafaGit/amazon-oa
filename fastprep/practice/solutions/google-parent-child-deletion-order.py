# Kahn topological sort on child -> parent edges with a min-heap for smallest-id tie breaking.
import heapq
from typing import List, Optional, Any


def deletionOrder(n: int, parentChild: List[List[int]]) -> List[int]:
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for p, c in parentChild:
        adj[c].append(p)
        indeg[p] += 1

    heap = [i for i in range(n) if indeg[i] == 0]
    heapq.heapify(heap)
    order: List[int] = []
    while heap:
        node = heapq.heappop(heap)
        order.append(node)
        for nxt in adj[node]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)
    return order

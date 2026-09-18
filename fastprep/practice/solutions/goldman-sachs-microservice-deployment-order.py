# Kahn topological sort with a min-heap to always pick the smallest ready label.
from typing import List, Optional, Any
import heapq


def deploymentOrder(n: int, dependencies: List[List[int]]) -> List[int]:
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for service, prereq in dependencies:
        adj[prereq].append(service)
        indeg[service] += 1

    heap = [i for i in range(n) if indeg[i] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        node = heapq.heappop(heap)
        order.append(node)
        for nxt in adj[node]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)

    return order if len(order) == n else []

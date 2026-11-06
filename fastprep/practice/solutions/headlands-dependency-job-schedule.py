from typing import List, Optional, Any
from collections import deque


def earliestSchedule(durations: List[int], dependencies: List[List[int]]) -> List[int]:
    n = len(durations)
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for before, after in dependencies:
        adj[before].append(after)
        indeg[after] += 1
    start = [0] * n
    q = deque(i for i in range(n) if indeg[i] == 0)
    while q:
        u = q.popleft()
        finish = start[u] + durations[u]
        for v in adj[u]:
            if finish > start[v]:
                start[v] = finish
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    out = []
    for i in range(n):
        out.append(start[i])
        out.append(start[i] + durations[i])
    return out

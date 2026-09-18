from typing import List, Optional, Any
from collections import deque


def solve(durations: List[int], dependencies: List[List[int]]) -> int:
    n = len(durations)
    if n == 0:
        return 0
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for dep in dependencies:
        before, after = dep[0], dep[1]
        adj[before].append(after)
        indeg[after] += 1

    # finish[v] = earliest time task v can finish
    finish = [0] * n
    q = deque()
    for v in range(n):
        if indeg[v] == 0:
            finish[v] = durations[v]
            q.append(v)

    processed = 0
    while q:
        u = q.popleft()
        processed += 1
        for v in adj[u]:
            # v cannot start before u finishes
            if finish[u] + durations[v] > finish[v]:
                finish[v] = finish[u] + durations[v]
            indeg[v] -= 1
            if indeg[v] == 0:
                if finish[v] < durations[v]:
                    finish[v] = durations[v]
                q.append(v)

    return max(finish) if finish else 0

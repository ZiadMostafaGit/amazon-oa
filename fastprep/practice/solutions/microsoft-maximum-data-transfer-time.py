from collections import deque
from typing import List


def getMaxTime(g_nodes: int, g_from: List[int], g_to: List[int]) -> int:
    adj = [[] for _ in range(g_nodes + 1)]
    for a, b in zip(g_from, g_to):
        adj[a].append(b)
        adj[b].append(a)

    def farthest(s):
        d = [-1] * (g_nodes + 1)
        d[s] = 0
        q = deque([s])
        last = s
        while q:
            x = q.popleft()
            last = x
            for y in adj[x]:
                if d[y] < 0:
                    d[y] = d[x] + 1
                    q.append(y)
        return last, d[last]

    a, _ = farthest(1)
    _, diameter = farthest(a)
    return diameter

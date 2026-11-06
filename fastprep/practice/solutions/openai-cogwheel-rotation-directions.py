from typing import List, Optional, Any
from collections import deque


def countRotations(nCogwheels: int, connections: List[List[int]]) -> List[int]:
    adj = [[] for _ in range(nCogwheels)]
    for u, v in connections:
        adj[u].append(v)
        adj[v].append(u)
    side = [-1] * nCogwheels
    side[0] = 0
    q = deque([0])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if side[v] == -1:
                side[v] = side[u] ^ 1
                q.append(v)
            elif side[v] == side[u]:
                return [-1, -1]
    cw = side.count(0)
    return [cw, nCogwheels - cw - side.count(-1)]

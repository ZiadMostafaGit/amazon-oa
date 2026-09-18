# BFS from the start city over the undirected tree; answer is the eccentricity of start.
from collections import deque
from typing import List, Optional, Any


def minutesToInfectTree(graph: List[str], start: int) -> int:
    adj = {}
    for edge in graph:
        u_s, v_s = edge.split("->")
        u, v = int(u_s.strip()), int(v_s.strip())
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)

    if start not in adj:
        return 0

    seen = {start}
    q = deque([start])
    minutes = -1
    while q:
        minutes += 1
        for _ in range(len(q)):
            node = q.popleft()
            for nxt in adj[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
    return minutes

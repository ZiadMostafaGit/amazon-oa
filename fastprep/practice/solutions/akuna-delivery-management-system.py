# BFS from the company for shortest hop counts, then sort reachable cities by (distance, id).
from typing import List, Optional, Any
from collections import deque


def order(cityNodes: int, cityFrom: List[int], cityTo: List[int], company: int) -> List[int]:
    adj = [[] for _ in range(cityNodes + 1)]
    for a, b in zip(cityFrom, cityTo):
        adj[a].append(b)
        adj[b].append(a)

    dist = [-1] * (cityNodes + 1)
    dist[company] = 0
    queue = deque([company])
    while queue:
        node = queue.popleft()
        for nxt in adj[node]:
            if dist[nxt] == -1:
                dist[nxt] = dist[node] + 1
                queue.append(nxt)

    reachable = [c for c in range(1, cityNodes + 1) if c != company and dist[c] != -1]
    reachable.sort(key=lambda c: (dist[c], c))
    return reachable

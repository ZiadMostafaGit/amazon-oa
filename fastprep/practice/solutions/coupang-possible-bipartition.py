# BFS 2-coloring of the dislike graph; false if any edge joins same-colored nodes.
from typing import List, Optional, Any
from collections import deque


def possibleBipartition(n: int, dislikes: List[List[int]]) -> bool:
    adj = [[] for _ in range(n + 1)]
    for a, b in dislikes:
        adj[a].append(b)
        adj[b].append(a)

    color = [0] * (n + 1)
    for start in range(1, n + 1):
        if color[start] != 0:
            continue
        color[start] = 1
        queue = deque([start])
        while queue:
            u = queue.popleft()
            cu = color[u]
            for v in adj[u]:
                if color[v] == 0:
                    color[v] = -cu
                    queue.append(v)
                elif color[v] == cu:
                    return False
    return True

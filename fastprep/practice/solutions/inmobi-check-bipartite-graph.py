# BFS two-coloring over the symmetrized adjacency matrix.
from typing import List, Optional, Any
from collections import deque


def isGraphBipartite(edges: List[List[int]]) -> bool:
    n = len(edges)
    adj = [[] for _ in range(n)]
    for i in range(n):
        row = edges[i]
        for j in range(i + 1, n):
            if row[j] == 1 or edges[j][i] == 1:
                adj[i].append(j)
                adj[j].append(i)
    color = [-1] * n
    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            cu = color[u]
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - cu
                    queue.append(v)
                elif color[v] == cu:
                    return False
    return True

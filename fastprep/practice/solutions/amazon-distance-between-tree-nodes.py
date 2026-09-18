# BFS from source over the undirected tree adjacency; the first time target is reached is the answer.
from collections import deque
from typing import List


def solve(treeNodes: int, treeFrom: List[int], treeTo: List[int], root: int, source: int, target: int) -> int:
    if source == target:
        return 0
    adj = [[] for _ in range(treeNodes + 1)]
    for a, b in zip(treeFrom, treeTo):
        adj[a].append(b)
        adj[b].append(a)
    dist = [-1] * (treeNodes + 1)
    dist[source] = 0
    q = deque([source])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                if v == target:
                    return dist[v]
                q.append(v)
    return -1

# Two BFS passes (from Tom and from Jerry); answer is the max Jerry distance among rooms he reaches no later than Tom.
from collections import deque
from typing import List, Optional, Any


def maxEscapeSeconds(roomCount: int, edges: List[List[int]], tomStart: int, jerryStart: int) -> int:
    adj = [[] for _ in range(roomCount)]
    for e in edges:
        a, b = e[0], e[1]
        adj[a].append(b)
        adj[b].append(a)

    def bfs(src):
        dist = [-1] * roomCount
        dist[src] = 0
        q = deque([src])
        while q:
            u = q.popleft()
            du = dist[u] + 1
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = du
                    q.append(v)
        return dist

    dt = bfs(tomStart)
    dj = bfs(jerryStart)

    best = 0
    for v in range(roomCount):
        if dj[v] != -1 and dt[v] != -1 and dj[v] <= dt[v]:
            if dj[v] > best:
                best = dj[v]
    return best

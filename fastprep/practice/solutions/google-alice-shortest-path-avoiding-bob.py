# Double BFS (dist from Alice, dist from Bob) + DP over the shortest-path DAG in order of
# Alice's distance: a node is usable only if Bob cannot reach it by the time Alice is there.
from collections import deque
from typing import List


def solve(n: int, edges: List[List[int]], aliceStart: int, bobStart: int, destination: int) -> bool:
    adj = [[] for _ in range(n)]
    for e in edges:
        u, v = e[0], e[1]
        adj[u].append(v)
        adj[v].append(u)

    INF = float('inf')

    def bfs(src):
        dist = [INF] * n
        dist[src] = 0
        q = deque([src])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if dist[w] == INF:
                    dist[w] = dist[u] + 1
                    q.append(w)
        return dist

    dA = bfs(aliceStart)
    dB = bfs(bobStart)

    if dA[destination] == INF:
        return False

    # safe[v]: Alice can be at v at time dA[v] on a shortest path without ever being caught
    order = [v for v in range(n) if dA[v] != INF]
    order.sort(key=lambda v: dA[v])

    safe = [False] * n
    for v in order:
        if dB[v] <= dA[v]:
            continue
        if v == aliceStart:
            safe[v] = True
            continue
        for u in adj[v]:
            if dA[u] == dA[v] - 1 and safe[u]:
                safe[v] = True
                break

    return safe[destination]

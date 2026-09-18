# BFS from each key cell for pairwise distances, then bitmask TSP over start + deliveries.
from typing import List, Optional, Any
from collections import deque


def shortestDeliveryRoundTrip(grid: List[str]) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    start = None
    deliveries = []
    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if ch == 'S':
                start = (r, c)
            elif ch == 'D':
                deliveries.append((r, c))
    if start is None:
        return -1
    nodes = [start] + deliveries
    m = len(deliveries)
    if m == 0:
        return 0

    def bfs(src):
        dist = [[-1] * cols for _ in range(rows)]
        sr, sc = src
        dist[sr][sc] = 0
        q = deque([src])
        while q:
            r, c = q.popleft()
            d = dist[r][c] + 1
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#' and dist[nr][nc] < 0:
                    dist[nr][nc] = d
                    q.append((nr, nc))
        return dist

    n = len(nodes)
    INF = float('inf')
    cost = [[INF] * n for _ in range(n)]
    for i, node in enumerate(nodes):
        dist = bfs(node)
        for j, (r, c) in enumerate(nodes):
            if dist[r][c] >= 0:
                cost[i][j] = dist[r][c]

    for j in range(1, n):
        if cost[0][j] == INF:
            return -1

    full = 1 << m
    dp = [[INF] * m for _ in range(full)]
    for j in range(m):
        dp[1 << j][j] = cost[0][j + 1]
    for mask in range(full):
        row = dp[mask]
        for j in range(m):
            cur = row[j]
            if cur == INF:
                continue
            for t in range(m):
                if mask & (1 << t):
                    continue
                w = cost[j + 1][t + 1]
                if w == INF:
                    continue
                nm = mask | (1 << t)
                if cur + w < dp[nm][t]:
                    dp[nm][t] = cur + w

    best = INF
    for j in range(m):
        if dp[full - 1][j] != INF and cost[j + 1][0] != INF:
            best = min(best, dp[full - 1][j] + cost[j + 1][0])
    return -1 if best == INF else best

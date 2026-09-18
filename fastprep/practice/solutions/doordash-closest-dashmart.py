# Multi-source BFS from every DashMart; blocked queries take one manual first step.
from typing import List, Optional, Any
from collections import deque


def closestDashMart(city: List[List[str]], locations: List[List[int]]) -> List[int]:
    rows = len(city)
    cols = len(city[0]) if rows else 0
    INF = float('inf')
    dist = [[INF] * cols for _ in range(rows)]
    q = deque()
    for r in range(rows):
        for c in range(cols):
            if city[r][c] == 'D':
                dist[r][c] = 0
                q.append((r, c))
    while q:
        r, c = q.popleft()
        d = dist[r][c] + 1
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < rows and 0 <= nc < cols and city[nr][nc] != 'X' and dist[nr][nc] > d:
                dist[nr][nc] = d
                q.append((nr, nc))

    out: List[int] = []
    for loc in locations:
        r, c = loc[0], loc[1]
        if not (0 <= r < rows and 0 <= c < cols):
            out.append(-1)
            continue
        if city[r][c] != 'X':
            out.append(-1 if dist[r][c] == INF else dist[r][c])
            continue
        best = INF
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < rows and 0 <= nc < cols and city[nr][nc] != 'X':
                if dist[nr][nc] + 1 < best:
                    best = dist[nr][nc] + 1
        out.append(-1 if best == INF else best)
    return out

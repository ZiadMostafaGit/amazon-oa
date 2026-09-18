# Multi-source BFS for distance to nearest thief, then a max-min (widest path)
# Dijkstra with a max-heap from (0,0) to (n-1,n-1).
import heapq
from collections import deque
from typing import List


def solve(grid: List[List[int]]) -> int:
    n = len(grid)
    dist = [[-1] * n for _ in range(n)]
    q = deque()
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                dist[i][j] = 0
                q.append((i, j))
    if not q:
        return 2 * (n - 1)
    while q:
        x, y = q.popleft()
        d = dist[x][y]
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < n and 0 <= ny < n and dist[nx][ny] == -1:
                dist[nx][ny] = d + 1
                q.append((nx, ny))

    if n == 1:
        return dist[0][0]
    best = [[-1] * n for _ in range(n)]
    best[0][0] = dist[0][0]
    pq = [(-dist[0][0], 0, 0)]
    while pq:
        negv, x, y = heapq.heappop(pq)
        v = -negv
        if v < best[x][y]:
            continue
        if x == n - 1 and y == n - 1:
            return v
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < n and 0 <= ny < n:
                nv = v if v < dist[nx][ny] else dist[nx][ny]
                if nv > best[nx][ny]:
                    best[nx][ny] = nv
                    heapq.heappush(pq, (-nv, nx, ny))
    return 0

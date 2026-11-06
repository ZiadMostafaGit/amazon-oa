from typing import List, Optional, Any
from collections import deque
import heapq


def maximumSafenessFactor(grid: List[List[int]]) -> int:
    n = len(grid)
    dist = [[-1] * n for _ in range(n)]
    q = deque()
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                dist[r][c] = 0
                q.append((r, c))
    while q:
        r, c = q.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < n and 0 <= nc < n and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    best = [[-1] * n for _ in range(n)]
    best[0][0] = dist[0][0]
    pq = [(-dist[0][0], 0, 0)]
    while pq:
        s, r, c = heapq.heappop(pq)
        s = -s
        if r == n - 1 and c == n - 1:
            return s
        if s < best[r][c]:
            continue
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < n and 0 <= nc < n:
                ns = min(s, dist[nr][nc])
                if ns > best[nr][nc]:
                    best[nr][nc] = ns
                    heapq.heappush(pq, (-ns, nr, nc))
    return best[n - 1][n - 1]

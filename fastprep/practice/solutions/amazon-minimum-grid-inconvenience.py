# Multi-source 8-neighbour BFS for Chebyshev distances, then binary search the answer
# using the fact that one extra centre covers a set iff its row/col spans are <= 2d.
from typing import List, Optional, Any
from collections import deque


def solve(grid: List[List[int]]) -> int:
    rows = len(grid)
    if rows == 0:
        return 0
    cols = len(grid[0])
    if cols == 0:
        return 0

    INF = float('inf')
    dist = [[INF] * cols for _ in range(rows)]
    q = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                dist[r][c] = 0
                q.append((r, c))
    while q:
        r, c = q.popleft()
        d = dist[r][c] + 1
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] > d:
                    dist[nr][nc] = d
                    q.append((nr, nc))

    zeros = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]
    if not zeros:
        return 0

    def feasible(d: int) -> bool:
        minr = minc = None
        maxr = maxc = None
        for r, c in zeros:
            if dist[r][c] > d:
                if minr is None:
                    minr = maxr = r
                    minc = maxc = c
                else:
                    if r < minr:
                        minr = r
                    if r > maxr:
                        maxr = r
                    if c < minc:
                        minc = c
                    if c > maxc:
                        maxc = c
        if minr is None:
            return True
        return (maxr - minr) <= 2 * d and (maxc - minc) <= 2 * d

    lo, hi = 0, max(rows, cols)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

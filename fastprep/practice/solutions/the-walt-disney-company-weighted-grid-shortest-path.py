# Dijkstra over grid cells with per-direction edge weights.
import heapq
from typing import List, Optional, Any


def minimumTravelCost(grid: List[str], directionCosts: List[int]) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    start = end = None
    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if ch == 'S':
                start = (r, c)
            elif ch == 'T':
                end = (r, c)
    if start is None or end is None:
        return -1
    # up, right, down, left
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    INF = float('inf')
    dist = [[INF] * cols for _ in range(rows)]
    dist[start[0]][start[1]] = 0
    pq = [(0, start[0], start[1])]
    while pq:
        d, r, c = heapq.heappop(pq)
        if d > dist[r][c]:
            continue
        if (r, c) == end:
            return d
        for i, (dr, dc) in enumerate(moves):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                nd = d + directionCosts[i]
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heapq.heappush(pq, (nd, nr, nc))
    return -1

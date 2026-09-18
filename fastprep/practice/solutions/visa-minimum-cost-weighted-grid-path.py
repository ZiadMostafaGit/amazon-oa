# Dijkstra over grid cells with four-directional moves, node weight paid on entry.
from typing import List, Optional, Any
import heapq


def minimumWeightedGridPathCost(grid: List[List[int]]) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if rows == 0 or cols == 0:
        return -1
    if grid[0][0] == -1 or grid[rows - 1][cols - 1] == -1:
        return -1

    INF = float('inf')
    dist = [[INF] * cols for _ in range(rows)]
    dist[0][0] = grid[0][0]
    heap = [(grid[0][0], 0, 0)]
    while heap:
        d, r, c = heapq.heappop(heap)
        if d > dist[r][c]:
            continue
        if r == rows - 1 and c == cols - 1:
            return d
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < rows and 0 <= nc < cols:
                w = grid[nr][nc]
                if w == -1:
                    continue
                nd = d + w
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heapq.heappush(heap, (nd, nr, nc))
    return -1

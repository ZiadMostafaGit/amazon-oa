from typing import List, Optional, Any
import heapq


def swimInWater(grid: List[List[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    heap = [(grid[0][0], 0, 0)]
    seen[0][0] = True
    while heap:
        cost, r, c = heapq.heappop(heap)
        if r == rows - 1 and c == cols - 1:
            return cost
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc]:
                seen[nr][nc] = True
                h = grid[nr][nc]
                heapq.heappush(heap, (cost if cost > h else h, nr, nc))
    return -1

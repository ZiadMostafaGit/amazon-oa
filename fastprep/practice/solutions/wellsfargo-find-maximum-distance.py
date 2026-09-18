# Multi-source BFS from every obstacle gives each cell's Manhattan clearance, then a
# max-heap bottleneck search maximises the minimum clearance along an S->E path.
import heapq
from typing import List, Optional, Any


def findMaximumDistance(grid: List[str]) -> int:
    rows = ["".join(ch for ch in row if not ch.isspace()) for row in grid]
    rows = [r for r in rows if r]
    n = len(rows)
    if n == 0:
        return 0
    m = max(len(r) for r in rows)

    INF = n + m + 1
    dist = [[INF] * m for _ in range(n)]
    queue = []
    start = end = None
    for r in range(n):
        row = rows[r]
        for c in range(m):
            ch = row[c] if c < len(row) else '.'
            if ch == '*':
                dist[r][c] = 0
                queue.append((r, c))
            elif ch == 'S':
                start = (r, c)
            elif ch == 'E':
                end = (r, c)

    if start is None or end is None:
        return 0

    # Multi-source BFS: on an unobstructed grid this yields the Manhattan distance
    # to the nearest obstacle.
    head = 0
    while head < len(queue):
        r, c = queue[head]
        head += 1
        d = dist[r][c] + 1
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < n and 0 <= nc < m and dist[nr][nc] > d:
                dist[nr][nc] = d
                queue.append((nr, nc))

    # Widest-bottleneck search: always expand the reachable cell with the largest
    # clearance seen so far on the way to it.
    best = [[-1] * m for _ in range(n)]
    sr, sc = start
    best[sr][sc] = dist[sr][sc]
    heap = [(-dist[sr][sc], sr, sc)]
    while heap:
        neg, r, c = heapq.heappop(heap)
        value = -neg
        if value < best[r][c]:
            continue
        if (r, c) == end:
            return value
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < n and 0 <= nc < m:
                cand = value if value < dist[nr][nc] else dist[nr][nc]
                if cand > best[nr][nc]:
                    best[nr][nc] = cand
                    heapq.heappush(heap, (-cand, nr, nc))
    return -1

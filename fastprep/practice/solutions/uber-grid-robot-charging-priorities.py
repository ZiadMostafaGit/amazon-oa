# Dijkstra over (cell, battery) with lexicographic (visits, moves) cost, plus a
# binary search on the battery capacity (visits are monotone non-increasing in it).
import heapq
from typing import List, Optional, Any

_DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def _solve(grid, rows, cols, start, target, capacity):
    """Min (charging visits, moves) reaching target with the given capacity, or None."""
    inf = (float('inf'), float('inf'))
    size = rows * cols
    dist = [[inf] * (capacity + 1) for _ in range(size)]
    dist[start][capacity] = (0, 0)
    heap = [(0, 0, start, capacity)]
    while heap:
        visits, moves, idx, batt = heapq.heappop(heap)
        if dist[idx][batt] != (visits, moves):
            continue
        if idx == target:
            return (visits, moves)
        if batt == 0:
            continue
        r, c = divmod(idx, cols)
        for dr, dc in _DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                ch = grid[nr][nc]
                if ch == '#':
                    continue
                if ch == 'C':
                    nvisits, nbatt = visits + 1, capacity
                else:
                    nvisits, nbatt = visits, batt - 1
                cand = (nvisits, moves + 1)
                ni = nr * cols + nc
                if cand < dist[ni][nbatt]:
                    dist[ni][nbatt] = cand
                    heapq.heappush(heap, (cand[0], cand[1], ni, nbatt))
    return None


def optimalChargingCost(grid: List[str]) -> List[int]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    start = target = -1
    for r in range(rows):
        row = grid[r]
        for c in range(cols):
            if row[c] == 'S':
                start = r * cols + c
            elif row[c] == 'T':
                target = r * cols + c
    if start < 0 or target < 0:
        return [-1, -1, -1]

    # Any segment can be shortened to a simple path, so this capacity is always enough.
    cap_max = rows * cols
    best = _solve(grid, rows, cols, start, target, cap_max)
    if best is None:
        return [-1, -1, -1]
    min_visits = best[0]

    lo, hi = 1, cap_max
    while lo < hi:
        mid = (lo + hi) // 2
        got = _solve(grid, rows, cols, start, target, mid)
        if got is not None and got[0] == min_visits:
            hi = mid
        else:
            lo = mid + 1
    final = _solve(grid, rows, cols, start, target, lo)
    return [min_visits, lo, final[1]]

# BFS distances from the start, then greedy: take the smallest letter whose cell can still return in the steps left.
from collections import deque
from typing import List

MOVES = (('D', 1, 0), ('L', 0, -1), ('R', 0, 1), ('U', -1, 0))


def solve(grid: List[str], k: int) -> str:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    sr = sc = -1
    for r in range(rows):
        row = grid[r]
        for c in range(cols):
            if c < len(row) and row[c] == 'x':
                sr, sc = r, c
    if sr < 0:
        return ""
    if k == 0:
        return ""
    if k % 2 == 1:
        return ""

    def free(r, c):
        return 0 <= r < rows and 0 <= c < cols and c < len(grid[r]) and grid[r][c] != '#'

    INF = float('inf')
    dist = [[INF] * cols for _ in range(rows)]
    dist[sr][sc] = 0
    dq = deque([(sr, sc)])
    while dq:
        r, c = dq.popleft()
        d = dist[r][c] + 1
        for _, dr, dc in MOVES:
            nr, nc = r + dr, c + dc
            if free(nr, nc) and dist[nr][nc] > d:
                dist[nr][nc] = d
                dq.append((nr, nc))

    start_has_neighbor = any(free(sr + dr, sc + dc) for _, dr, dc in MOVES)

    def feasible(r, c, m):
        d = dist[r][c]
        if d is INF or d > m or (m - d) % 2:
            return False
        if m == d:
            return True
        return d > 0 or start_has_neighbor

    if not feasible(sr, sc, k):
        return ""

    out = []
    r, c = sr, sc
    for step in range(k):
        left = k - step - 1
        for ch, dr, dc in MOVES:
            nr, nc = r + dr, c + dc
            if free(nr, nc) and feasible(nr, nc, left):
                out.append(ch)
                r, c = nr, nc
                break
        else:
            return ""
    return "".join(out)

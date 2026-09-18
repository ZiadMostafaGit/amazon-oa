# BFS distances from target, then greedy walk picking the lexicographically smallest next cell.
from collections import deque
from typing import List, Optional, Any


def findExploredPath(hiddenMap: List[str], start: List[int], target: List[int]) -> List[List[int]]:
    rows = len(hiddenMap)
    cols = len(hiddenMap[0]) if rows else 0
    sr, sc = start[0], start[1]
    tr, tc = target[0], target[1]
    if rows == 0 or cols == 0:
        return []
    if hiddenMap[sr][sc] == '#' or hiddenMap[tr][tc] == '#':
        return []

    INF = float('inf')
    dist = [[INF] * cols for _ in range(rows)]
    dist[tr][tc] = 0
    q = deque([(tr, tc)])
    while q:
        r, c = q.popleft()
        d = dist[r][c] + 1
        for nr, nc in ((r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)):
            if 0 <= nr < rows and 0 <= nc < cols and hiddenMap[nr][nc] == '.' and dist[nr][nc] > d:
                dist[nr][nc] = d
                q.append((nr, nc))

    if dist[sr][sc] == INF:
        return []

    path = [[sr, sc]]
    r, c = sr, sc
    while (r, c) != (tr, tc):
        want = dist[r][c] - 1
        for nr, nc in ((r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)):
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == want:
                r, c = nr, nc
                break
        path.append([r, c])
    return path

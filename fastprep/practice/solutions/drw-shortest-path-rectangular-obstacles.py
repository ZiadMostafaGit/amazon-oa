# 2D difference array to paint rectangular obstacles, then BFS over the free cells.
from collections import deque
from typing import List, Optional, Any


def solution(N: int, M: int, X1: List[int], Y1: List[int], X2: List[int], Y2: List[int]) -> int:
    if N <= 0 or M <= 0:
        return -1
    diff = [[0] * (M + 1) for _ in range(N + 1)]
    k = len(X1)
    for i in range(k):
        x1, y1, x2, y2 = X1[i], Y1[i], X2[i], Y2[i]
        if x1 > x2 or y1 > y2:
            continue
        x1 = max(x1, 0)
        y1 = max(y1, 0)
        x2 = min(x2, N - 1)
        y2 = min(y2, M - 1)
        if x1 > x2 or y1 > y2:
            continue
        diff[x1][y1] += 1
        diff[x1][y2 + 1] -= 1
        diff[x2 + 1][y1] -= 1
        diff[x2 + 1][y2 + 1] += 1

    blocked = [[False] * M for _ in range(N)]
    for x in range(N):
        row = diff[x]
        prev = diff[x - 1] if x > 0 else None
        running = 0
        for y in range(M):
            if prev is not None:
                row[y] += prev[y]
            running += row[y]
            if running > 0:
                blocked[x][y] = True

    if blocked[0][0] or blocked[N - 1][M - 1]:
        return -1
    if N == 1 and M == 1:
        return 0

    dist = [[-1] * M for _ in range(N)]
    dist[0][0] = 0
    q = deque([(0, 0)])
    while q:
        x, y = q.popleft()
        d = dist[x][y]
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < N and 0 <= ny < M and dist[nx][ny] == -1 and not blocked[nx][ny]:
                if nx == N - 1 and ny == M - 1:
                    return d + 1
                dist[nx][ny] = d + 1
                q.append((nx, ny))
    return -1

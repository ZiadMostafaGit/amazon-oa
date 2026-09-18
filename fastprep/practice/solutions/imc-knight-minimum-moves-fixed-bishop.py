# BFS over knight moves on squares not attacked by the fixed bishop.
from collections import deque


def minKnightMoves(n: int, startRow: int, startCol: int, endRow: int, endCol: int, bishopRow: int, bishopCol: int) -> int:
    def safe(r, c):
        if r < 0 or c < 0 or r >= n or c >= n:
            return False
        if r - c == bishopRow - bishopCol:
            return False
        if r + c == bishopRow + bishopCol:
            return False
        return True

    if not safe(startRow, startCol) or not safe(endRow, endCol):
        return -1
    if startRow == endRow and startCol == endCol:
        return 0

    moves = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))
    dist = [[-1] * n for _ in range(n)]
    dist[startRow][startCol] = 0
    q = deque([(startRow, startCol)])
    while q:
        r, c = q.popleft()
        d = dist[r][c]
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if safe(nr, nc) and dist[nr][nc] == -1:
                if nr == endRow and nc == endCol:
                    return d + 1
                dist[nr][nc] = d + 1
                q.append((nr, nc))
    return -1

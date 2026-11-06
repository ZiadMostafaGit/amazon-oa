# BFS over (square, bishop captured?) states.
from collections import deque


def minKnightMoves(n: int, startRow: int, startCol: int, endRow: int, endCol: int, bishopRow: int, bishopCol: int) -> int:
    if startRow == endRow and startCol == endCol:
        return 0
    br, bc = bishopRow, bishopCol

    def threatened(r, c):
        return r - c == br - bc or r + c == br + bc

    cap0 = 1 if (startRow == br and startCol == bc) else 0
    moves = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))
    seen = [[[False] * n for _ in range(n)] for _ in range(2)]
    seen[cap0][startRow][startCol] = True
    q = deque([(startRow, startCol, cap0, 0)])
    while q:
        r, c, cap, d = q.popleft()
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < n and 0 <= nc < n):
                continue
            if nr == endRow and nc == endCol:
                return d + 1
            ncap = cap
            if not cap:
                if nr == br and nc == bc:
                    ncap = 1
                elif threatened(nr, nc):
                    continue
            if not seen[ncap][nr][nc]:
                seen[ncap][nr][nc] = True
                q.append((nr, nc, ncap, d + 1))
    return -1

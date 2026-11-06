# One simultaneous step: count each cell's eight neighbours on the ORIGINAL board, write into a new board.
from typing import List


def gameOfLife(board: List[List[int]]) -> List[List[int]]:
    m, n = len(board), len(board[0])
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    out = [[0] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            live = 0
            for dr, dc in dirs:
                rr, cc = r + dr, c + dc
                if 0 <= rr < m and 0 <= cc < n:
                    live += board[rr][cc]
            if board[r][c] == 1:
                out[r][c] = 1 if live in (2, 3) else 0
            else:
                out[r][c] = 1 if live == 3 else 0
    return out

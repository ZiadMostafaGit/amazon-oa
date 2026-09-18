# Iterative BFS flood fill over the 8-neighborhood, stopping at cells with a positive mine clue.
from collections import deque
from typing import List, Optional, Any


def revealRegion(board: List[List[int]], startRow: int, startCol: int) -> List[List[int]]:
    rows = len(board)
    cols = len(board[0]) if rows else 0
    if not rows or not cols:
        return board
    if board[startRow][startCol] != 0:
        return board

    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    queue = deque([(startRow, startCol)])
    seen = {(startRow, startCol)}
    while queue:
        r, c = queue.popleft()
        mines = 0
        neighbors = []
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if board[nr][nc] == -1:
                    mines += 1
                else:
                    neighbors.append((nr, nc))
        if mines > 0:
            board[r][c] = mines
        else:
            board[r][c] = -2
            for nr, nc in neighbors:
                if board[nr][nc] == 0 and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    queue.append((nr, nc))
    return board

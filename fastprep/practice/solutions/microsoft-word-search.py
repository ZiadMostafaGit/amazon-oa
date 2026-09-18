# Backtracking DFS from every cell with in-place visited marking.
from typing import List, Optional, Any


def wordExists(board: List[List[str]], word: str) -> bool:
    if not word:
        return True
    if not board or not board[0]:
        return False
    rows, cols = len(board), len(board[0])
    if rows * cols < len(word):
        return False
    grid = [list(r) for r in board]

    def dfs(r: int, c: int, k: int) -> bool:
        if grid[r][c] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        tmp = grid[r][c]
        grid[r][c] = '\0'
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dfs(nr, nc, k + 1):
                grid[r][c] = tmp
                return True
        grid[r][c] = tmp
        return False

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False

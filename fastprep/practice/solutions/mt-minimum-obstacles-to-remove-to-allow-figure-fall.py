from typing import List, Optional, Any


def minimumObstaclesToRemoveToAllowFigureFall(matrix: List[List[str]]) -> int:
    rows = len(matrix)
    if rows == 0:
        return 0
    cols = len(matrix[0])
    lowest = max(r for r in range(rows) for c in range(cols) if matrix[r][c] == '*')
    d = rows - 1 - lowest  # how far the figure has to fall
    if d == 0:
        return 0
    removed = 0
    for c in range(cols):
        # cell (r, c) of the figure sweeps rows r+1 .. r+d of this column
        diff = [0] * (rows + 1)
        for r in range(rows):
            if matrix[r][c] == '*':
                diff[r + 1] += 1
                diff[min(rows, r + d + 1)] -= 1
        cover = 0
        for r in range(rows):
            cover += diff[r]
            if cover > 0 and matrix[r][c] == '#':
                removed += 1
    return removed

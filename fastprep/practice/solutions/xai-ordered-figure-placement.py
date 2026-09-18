# Greedy row-major scan: for each figure try anchors in (row, col) order and place at the first that fits.
from typing import List


SHAPES = {
    "A": [(0, 0)],
    "B": [(0, 0), (0, 1), (0, 2)],
    "C": [(0, 0), (0, 1), (1, 0), (1, 1)],
    "D": [(0, 0), (1, 0), (1, 1), (2, 0)],
    "E": [(0, 1), (1, 0), (1, 1), (1, 2)],
}


def placeFigures(n: int, m: int, figures: List[str]) -> List[List[int]]:
    grid = [[0] * m for _ in range(n)]
    for idx, name in enumerate(figures):
        cells = SHAPES[str(name)]
        placed = False
        for r in range(n):
            if placed:
                break
            for c in range(m):
                ok = True
                for dr, dc in cells:
                    rr, cc = r + dr, c + dc
                    if rr < 0 or rr >= n or cc < 0 or cc >= m or grid[rr][cc] != 0:
                        ok = False
                        break
                if ok:
                    for dr, dc in cells:
                        grid[r + dr][c + dc] = idx + 1
                    placed = True
                    break
    return grid

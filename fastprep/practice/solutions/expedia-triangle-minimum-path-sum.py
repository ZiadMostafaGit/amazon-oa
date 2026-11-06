# Bottom-up: best[c] = triangle[r][c] + min(best[c], best[c+1]) from the row below.
from typing import List


def minimumTrianglePath(triangle: List[List[int]]) -> int:
    best = list(triangle[-1])
    for r in range(len(triangle) - 2, -1, -1):
        best = [triangle[r][c] + min(best[c], best[c + 1]) for c in range(r + 1)]
    return best[0]

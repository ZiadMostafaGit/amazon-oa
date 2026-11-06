# side[r][c] = largest all-ones square with bottom-right corner (r, c); it also counts the squares ending there.
from typing import List


def countSquares(matrix: List[List[int]]) -> int:
    cols = len(matrix[0])
    prev = [0] * (cols + 1)
    total = 0
    for row in matrix:
        cur = [0] * (cols + 1)
        for c in range(1, cols + 1):
            if row[c - 1]:
                cur[c] = 1 + min(prev[c], cur[c - 1], prev[c - 1])
                total += cur[c]
        prev = cur
    return total

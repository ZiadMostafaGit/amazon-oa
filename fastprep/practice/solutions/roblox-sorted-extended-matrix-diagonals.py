# Build each of the 2n-1 diagonals, repeat it cyclically to length n, then stable-sort the strings.
from typing import List, Optional, Any


def solution(matrix: List[List[str]]) -> List[int]:
    n = len(matrix)
    diagonals: List[List[str]] = [[] for _ in range(2 * n - 1)]
    # Diagonal index (1-based) of cell (i, j) is j - i + n; traverse top-to-bottom.
    for i in range(n):
        for j in range(n):
            diagonals[j - i + n - 1].append(matrix[i][j])
    keys = []
    for idx, cells in enumerate(diagonals):
        length = len(cells)
        word = "".join(cells[k % length] for k in range(n))
        keys.append((word, idx + 1))
    keys.sort(key=lambda pair: pair[0])
    return [idx for _, idx in keys]

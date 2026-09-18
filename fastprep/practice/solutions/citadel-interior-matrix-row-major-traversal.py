# Direct row-major scan over the non-boundary index ranges.
from typing import List, Optional, Any


def traverseInteriorCells(matrix: List[List[int]]) -> List[int]:
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    if rows < 3 or cols < 3:
        return []
    out = []
    for r in range(1, rows - 1):
        row = matrix[r]
        out.extend(row[1:cols - 1])
    return out

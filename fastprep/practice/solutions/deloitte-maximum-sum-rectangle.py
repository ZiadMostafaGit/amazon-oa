# Kadane over every pair of column bounds using prefix row sums (O(cols^2 * rows)).
from typing import List, Optional, Any


def maximumSumRectangle(matrix: List[List[int]]) -> int:
    rows = len(matrix)
    cols = len(matrix[0])
    best = None
    for left in range(cols):
        acc = [0] * rows
        for right in range(left, cols):
            for r in range(rows):
                acc[r] += matrix[r][right]
            # Kadane on acc
            cur = 0
            for v in acc:
                cur = v if cur <= 0 else cur + v
                if best is None or cur > best:
                    best = cur
    return best

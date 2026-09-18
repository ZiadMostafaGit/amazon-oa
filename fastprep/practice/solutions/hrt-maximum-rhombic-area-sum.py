# Row prefix sums; for each valid center add the horizontal slice of the diamond per row.
from typing import List, Optional, Any


def maximumRhombicSum(matrix: List[List[int]], r: int) -> int:
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    pre = []
    for row in matrix:
        p = [0] * (cols + 1)
        for j, v in enumerate(row):
            p[j + 1] = p[j] + v
        pre.append(p)
    k = r - 1
    best = None
    for cr in range(k, rows - k):
        for cc in range(k, cols - k):
            total = 0
            for d in range(-k, k + 1):
                w = k - abs(d)
                p = pre[cr + d]
                total += p[cc + w + 1] - p[cc - w]
            if best is None or total > best:
                best = total
    return best if best is not None else 0

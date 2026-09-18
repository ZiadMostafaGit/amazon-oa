# Row prefix sums: each rhombus row is a contiguous segment, so every center costs O(r).
from typing import List, Optional, Any


def maximumRhombicSum(matrix: List[List[int]], r: int) -> int:
    n = len(matrix)
    m = len(matrix[0]) if n else 0
    if n == 0 or m == 0:
        return 0

    pre = []
    for row in matrix:
        acc = [0] * (m + 1)
        s = 0
        for j, v in enumerate(row):
            s += v
            acc[j + 1] = s
        pre.append(acc)

    d = r - 1
    best = None
    for cr in range(d, n - d):
        for cc in range(d, m - d):
            total = 0
            for row in range(cr - d, cr + d + 1):
                span = d - abs(row - cr)
                lo = cc - span
                hi = cc + span
                total += pre[row][hi + 1] - pre[row][lo]
            if best is None or total > best:
                best = total
    return 0 if best is None else best

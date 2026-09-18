# 2D prefix sums + binary search on k (max k x k sum is monotone since all entries are positive).
from typing import List, Optional, Any


def maxSize(matrix: List[List[int]], threshold: int) -> int:
    n = len(matrix)
    if n == 0:
        return 0
    m = len(matrix[0])
    pre = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        row = matrix[i]
        prev = pre[i]
        cur = pre[i + 1]
        run = 0
        for j in range(m):
            run += row[j]
            cur[j + 1] = prev[j + 1] + run

    def ok(k: int) -> bool:
        if k > n or k > m:
            return False
        for i in range(n - k + 1):
            top = pre[i]
            bot = pre[i + k]
            for j in range(m - k + 1):
                if bot[j + k] - bot[j] - top[j + k] + top[j] > threshold:
                    return False
        return True

    lo, hi, best = 1, min(n, m), 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if ok(mid):
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best

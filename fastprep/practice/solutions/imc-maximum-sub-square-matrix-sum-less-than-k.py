# Approach: 2D prefix sums plus binary search on the square size (max square sum grows with size).
from typing import List, Optional, Any


def maxSubSquareMatrixSumLessThanK(matrix: List[List[int]], k: int) -> int:
    n = len(matrix)
    if n == 0:
        return 0
    m = len(matrix[0])
    if m == 0:
        return 0
    size_limit = min(n, m)

    # prefix[i][j] = sum of matrix[0..i-1][0..j-1]
    prefix = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        row = matrix[i]
        prev = prefix[i]
        cur = prefix[i + 1]
        running = 0
        for j in range(m):
            running += row[j]
            cur[j + 1] = prev[j + 1] + running

    def all_squares_ok(s: int) -> bool:
        """True when every s x s square has sum <= k."""
        for i in range(n - s + 1):
            top = prefix[i]
            bot = prefix[i + s]
            for j in range(m - s + 1):
                total = bot[j + s] - bot[j] - top[j + s] + top[j]
                if total > k:
                    return False
        return True

    # entries are positive, so the maximum square sum is non-decreasing in s
    lo, hi, best = 1, size_limit, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if all_squares_ok(mid):
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best

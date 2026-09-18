# Prefix max / suffix min scan: a split is valid iff max(left) <= min(right).
from typing import List, Optional, Any


def solve(A: List[int]) -> int:
    n = len(A)
    if n < 2:
        return 0
    suffix_min = [0] * n
    suffix_min[n - 1] = A[n - 1]
    for i in range(n - 2, -1, -1):
        suffix_min[i] = A[i] if A[i] < suffix_min[i + 1] else suffix_min[i + 1]
    count = 0
    running_max = A[0]
    for i in range(1, n):
        if running_max <= suffix_min[i]:
            count += 1
        if A[i] > running_max:
            running_max = A[i]
    return count

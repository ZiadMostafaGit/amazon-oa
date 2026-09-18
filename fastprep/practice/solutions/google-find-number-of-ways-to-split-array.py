# Prefix maximum vs suffix minimum: a split works iff every left element <= every right element.
from typing import List, Optional, Any


def findNumberOfWaysToSplitArray(A: List[int]) -> int:
    n = len(A)
    if n < 2:
        return 0
    suffix_min = [0] * n
    cur = A[n - 1]
    for i in range(n - 1, -1, -1):
        if A[i] < cur:
            cur = A[i]
        suffix_min[i] = cur

    count = 0
    prefix_max = A[0]
    for i in range(1, n):
        if prefix_max <= suffix_min[i]:
            count += 1
        if A[i] > prefix_max:
            prefix_max = A[i]
    return count

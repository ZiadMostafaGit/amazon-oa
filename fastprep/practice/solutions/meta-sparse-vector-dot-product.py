# Two-pointer merge over the sorted index/value tuple lists.
from typing import List, Optional, Any


def sparseDotProduct(length: int, first: List[List[int]], second: List[List[int]]) -> int:
    i = 0
    j = 0
    total = 0
    n = len(first)
    m = len(second)
    while i < n and j < m:
        ai = first[i][0]
        bj = second[j][0]
        if ai == bj:
            total += first[i][1] * second[j][1]
            i += 1
            j += 1
        elif ai < bj:
            i += 1
        else:
            j += 1
    return total

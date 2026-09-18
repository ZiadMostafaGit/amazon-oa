# Greedy: every descent forces its right element into the selected set with x >= the drop; take x = max drop and validate.
from typing import List, Optional, Any


def getMinimumIncrement(arr: List[int]) -> int:
    n = len(arr)
    if n <= 1:
        return 0

    selected = [False] * n
    best = 0
    for i in range(n - 1):
        if arr[i] > arr[i + 1]:
            # Only assignment that can repair this pair is (0, x) with x >= drop.
            selected[i + 1] = True
            drop = arr[i] - arr[i + 1]
            if drop > best:
                best = drop

    if best == 0:
        return 0

    # Two adjacent forced elements cannot both be incremented.
    for i in range(n - 1):
        if selected[i] and selected[i + 1]:
            return -1

    x = best
    prev = arr[0] + (x if selected[0] else 0)
    for i in range(1, n):
        cur = arr[i] + (x if selected[i] else 0)
        if cur < prev:
            return -1
        prev = cur
    return x

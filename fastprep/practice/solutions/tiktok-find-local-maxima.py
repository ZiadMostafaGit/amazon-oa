# Precompute maximal strictly decreasing run lengths outward on each side, then compare against min(localArea, distance to edge).
from typing import List, Optional, Any


def findLocalMaxima(rawData: List[int], localArea: int) -> List[int]:
    n = len(rawData)
    # left[i]: how many steps we can walk left from i while values strictly decrease
    left = [0] * n
    for i in range(1, n):
        if rawData[i] > rawData[i - 1]:
            left[i] = left[i - 1] + 1
        else:
            left[i] = 0
    right = [0] * n
    for i in range(n - 2, -1, -1):
        if rawData[i] > rawData[i + 1]:
            right[i] = right[i + 1] + 1
        else:
            right[i] = 0
    res = []
    for i in range(n):
        need_l = min(localArea, i)
        need_r = min(localArea, n - 1 - i)
        if left[i] >= need_l and right[i] >= need_r:
            res.append(i)
    return res

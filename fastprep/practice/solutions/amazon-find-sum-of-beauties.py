# Build the concatenated array from de-duplicated ranges, then binary-search counts of smaller values.
from bisect import bisect_left
from typing import List, Optional, Any


def findSumOfBeauties(arr: List[int], pairs: List[List[int]]) -> int:
    n = len(arr)
    covered = [False] * n
    beautiful: List[int] = []
    seen = set()

    for p in pairs:
        if not p:
            continue
        l, r = p[0], p[1]
        if l > r:
            l, r = r, l
        if l < 0:
            l = 0
        if r > n - 1:
            r = n - 1
        if l > r:
            continue
        key = (l, r)
        if key in seen:
            continue
        seen.add(key)
        for i in range(l, r + 1):
            covered[i] = True
            beautiful.append(arr[i])

    ordered = sorted(beautiful)
    total = 0
    for i in range(n):
        if not covered[i]:
            total += bisect_left(ordered, arr[i])
    return total

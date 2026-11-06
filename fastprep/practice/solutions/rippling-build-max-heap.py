# Bottom-up heapify (Floyd): sift down every parent from n//2-1 to 0. O(n).
from typing import List, Optional, Any


def buildMaxHeap(nums: List[int]) -> List[int]:
    a = list(nums)
    n = len(a)
    for start in range(n // 2 - 1, -1, -1):
        i = start
        while True:
            l, r = 2 * i + 1, 2 * i + 2
            if l >= n:
                break
            c = l
            if r < n and a[r] > a[l]:
                c = r
            if a[c] > a[i]:
                a[i], a[c] = a[c], a[i]
                i = c
            else:
                break
    return a

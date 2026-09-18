# Standard next-permutation: find pivot from right, swap with successor, reverse suffix.
from typing import List, Optional, Any


def nextPermutation(nums: List[int]) -> List[int]:
    a = list(nums)
    n = len(a)
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i >= 0:
        j = n - 1
        while a[j] <= a[i]:
            j -= 1
        a[i], a[j] = a[j], a[i]
    lo, hi = i + 1, n - 1
    while lo < hi:
        a[lo], a[hi] = a[hi], a[lo]
        lo += 1
        hi -= 1
    return a

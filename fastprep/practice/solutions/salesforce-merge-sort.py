# Classic top-down merge sort with an auxiliary buffer merge.
from typing import List, Optional, Any


def mergeSort(nums: List[int]) -> List[int]:
    arr = list(nums)
    n = len(arr)
    if n < 2:
        return arr
    buf = [0] * n

    def sort(lo: int, hi: int) -> None:
        if hi - lo < 2:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid, hi)
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            if arr[j] < arr[i]:
                buf[k] = arr[j]
                j += 1
            else:
                buf[k] = arr[i]
                i += 1
            k += 1
        while i < mid:
            buf[k] = arr[i]
            i += 1
            k += 1
        while j < hi:
            buf[k] = arr[j]
            j += 1
            k += 1
        arr[lo:hi] = buf[lo:hi]

    import sys
    sys.setrecursionlimit(300000)
    sort(0, n)
    return arr

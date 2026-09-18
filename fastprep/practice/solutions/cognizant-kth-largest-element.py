# Quickselect (randomized pivot) for the kth largest element, average O(n).
import random
from typing import List


def findKthLargest(nums: List[int], k: int) -> int:
    arr = list(nums)
    target = len(arr) - k  # index in ascending order
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        pivot = arr[random.randint(lo, hi)]
        i, j, p = lo, hi, lo
        # three-way partition around pivot
        while p <= j:
            if arr[p] < pivot:
                arr[i], arr[p] = arr[p], arr[i]
                i += 1
                p += 1
            elif arr[p] > pivot:
                arr[p], arr[j] = arr[j], arr[p]
                j -= 1
            else:
                p += 1
        if target < i:
            hi = i - 1
        elif target > j:
            lo = j + 1
        else:
            return pivot
    return arr[lo]

# Brute force over all n cyclic shifts (n <= 200), summing |diff| per shift, then sort.
from typing import List, Optional, Any


def sortedCyclicShiftDifferences(nums1: List[int], nums2: List[int]) -> List[int]:
    n = len(nums1)
    sums = []
    for s in range(n):
        total = 0
        for i in range(n):
            total += abs(nums1[(i - s) % n] - nums2[i])
        sums.append(total)
    sums.sort()
    return sums

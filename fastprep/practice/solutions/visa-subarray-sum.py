# Contribution counting: element i appears in (i+1)*(n-i) subarrays.
from typing import List, Optional, Any


def getSubarraySum(n: int, arr: List[int]) -> int:
    total = 0
    for i in range(n):
        total += arr[i] * (i + 1) * (n - i)
    return total

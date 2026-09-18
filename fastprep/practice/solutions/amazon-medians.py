# Sort: with m = (k-1)//2 elements below the median, the best/worst medians are fixed positions.
from typing import List, Optional, Any


def medians(nums: List[int], k: int) -> List[int]:
    s = sorted(nums)
    n = len(s)
    m = (k - 1) // 2
    return [s[n - k + m], s[m]]

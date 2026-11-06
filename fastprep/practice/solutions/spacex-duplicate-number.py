# Values lie in 1..n-1, so each value names an index: negate nums[v] on first visit; a value whose index is already negative is the duplicate. O(n), O(1) extra.
from typing import List, Optional, Any


def findDuplicateNumber(nums: List[int]) -> int:
    a = list(nums)
    for x in a:
        v = abs(x)
        if a[v] < 0:
            return v
        a[v] = -a[v]
    return -1

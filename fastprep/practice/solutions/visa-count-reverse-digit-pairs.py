# Rearrange to nums[i]-flip(nums[i]) == nums[j]-flip(nums[j]); count pairs per key bucket.
from typing import List, Optional, Any


def countReverseDigitPairs(nums: List[int]) -> int:
    counts = {}
    for x in nums:
        key = x - int(str(x)[::-1])
        counts[key] = counts.get(key, 0) + 1
    return sum(c * (c + 1) // 2 for c in counts.values())

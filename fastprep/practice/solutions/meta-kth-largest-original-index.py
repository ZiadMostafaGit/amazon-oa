# Sort the indices, not the values: key (-nums[i], i) gives the rank order and keeps each original position. O(n log n).
from typing import List, Optional, Any


def kthLargestIndex(nums: List[int], k: int) -> int:
    order = sorted(range(len(nums)), key=lambda i: (-nums[i], i))
    return order[k - 1]

# Binary search on even indices: pairs align at even offsets before the single element and shift after it.
from typing import List, Optional, Any


def singleNonDuplicate(nums: List[int]) -> int:
    low, high = 0, len(nums) - 1
    while low < high:
        mid = (low + high) // 2
        if mid % 2 == 1:
            mid -= 1
        if nums[mid] == nums[mid + 1]:
            low = mid + 2
        else:
            high = mid
    return nums[low]

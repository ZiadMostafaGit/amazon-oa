# Prefix sums plus hash sets: for each split point, check if a removable value exists on either side.
from typing import List, Optional, Any


def canSplitAfterRemoval(nums: List[int]) -> bool:
    n = len(nums)
    total = sum(nums)

    # Case A: removed index lies in the left group.
    # left = nums[0:j] minus one element, right = nums[j:n]
    # need nums[i] = 2*prefix[j] - total, with i < j, j >= 2, j <= n-1
    seen = set()
    prefix = 0
    for j in range(1, n):
        prefix += nums[j - 1]
        seen.add(nums[j - 1])
        if j >= 2 and (2 * prefix - total) in seen:
            return True

    # Case B: removed index lies in the right group.
    # left = nums[0:j], right = nums[j:n] minus one element
    # need nums[i] = total - 2*prefix[j], with i >= j, j >= 1, j <= n-2
    seen = set()
    suffix_prefix = total
    for j in range(n - 1, 0, -1):
        seen.add(nums[j])
        suffix_prefix -= nums[j]  # suffix_prefix == prefix[j]
        if j <= n - 2 and (total - 2 * suffix_prefix) in seen:
            return True

    return False

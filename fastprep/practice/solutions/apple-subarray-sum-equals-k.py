from typing import List, Optional, Any


def countSubarrays(nums: List[int], k: int) -> int:
    seen = {0: 1}
    s = 0
    count = 0
    for v in nums:
        s += v
        count += seen.get(s - k, 0)
        seen[s] = seen.get(s, 0) + 1
    return count

# Sort indices by (value desc, index asc), take the first k indices, then restore original order.
from typing import List, Optional, Any


def retainTopKValues(nums: List[int], k: int) -> List[int]:
    if k <= 0:
        return []
    order = sorted(range(len(nums)), key=lambda i: (-nums[i], i))
    keep = sorted(order[:k])
    return [nums[i] for i in keep]

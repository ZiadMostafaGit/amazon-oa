# Binary search on the answer, greedily counting groups that fit under a candidate maximum.
from typing import List, Optional, Any


def minimizeLongestHike(segments: List[int], restStops: int) -> int:
    groups = restStops + 1

    def groups_needed(limit: int) -> int:
        count = 1
        current = 0
        for value in segments:
            if current + value > limit:
                count += 1
                current = value
            else:
                current += value
        return count

    low = max(segments)
    high = sum(segments)
    while low < high:
        mid = (low + high) // 2
        if groups_needed(mid) <= groups:
            high = mid
        else:
            low = mid + 1
    return low

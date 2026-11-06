# Bucket the values: points[v] = v * count(v). Then it is house robber over v = 1..max.
from typing import List, Optional, Any


def deleteAndEarn(nums: List[int]) -> int:
    if not nums:
        return 0
    points = [0] * (max(nums) + 1)
    for x in nums:
        points[x] += x
    take, skip = 0, 0
    for p in points:
        take, skip = skip + p, max(skip, take)
    return max(take, skip)

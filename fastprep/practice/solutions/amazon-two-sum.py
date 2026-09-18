# Value -> sorted index list, then scan i ascending and binary-search the first partner index > i.
from typing import List, Optional, Any
from bisect import bisect_right


def twoSum(nums: List[int], target: int) -> List[int]:
    positions = {}
    for idx, value in enumerate(nums):
        positions.setdefault(value, []).append(idx)
    for i, value in enumerate(nums):
        bucket = positions.get(target - value)
        if not bucket:
            continue
        p = bisect_right(bucket, i)
        if p < len(bucket):
            return [i, bucket[p]]
    return []

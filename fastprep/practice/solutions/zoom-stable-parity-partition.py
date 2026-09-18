# Stable partition: single pass collecting evens and odds separately, then concatenate.
from typing import List, Optional, Any


def partitionByParity(nums: List[int]) -> List[int]:
    evens = []
    odds = []
    for v in nums:
        if v % 2 == 0:
            evens.append(v)
        else:
            odds.append(v)
    return evens + odds

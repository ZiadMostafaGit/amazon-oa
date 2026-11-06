# A set of values seen so far: the first value already in the set is a duplicate. O(n).
from typing import List, Optional, Any


def containsDuplicate(nums: List[int]) -> bool:
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False

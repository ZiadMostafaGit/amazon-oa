# Frequency map, then count the keys whose frequency is exactly one.
from collections import Counter
from typing import List, Optional, Any


def countAppearingOnce(nums: List[int]) -> int:
    return sum(1 for c in Counter(nums).values() if c == 1)

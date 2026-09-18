# Counting: each distinct value can be placed at most once in each of the three monotone segments.
from typing import List, Optional, Any
from collections import Counter


def getMaximumEvents(payload: List[int]) -> int:
    freq = Counter(payload)
    return sum(min(c, 3) for c in freq.values())

# Distinct values in a set; each value a forms a pair when a + k is also in the set. O(n).
from typing import List, Optional, Any


def countPairs(numbers: List[int], k: int) -> int:
    values = set(numbers)
    return sum(1 for a in values if a + k in values)

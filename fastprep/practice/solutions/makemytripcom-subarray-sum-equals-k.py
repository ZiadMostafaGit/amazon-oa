# Prefix sums with a hash map counting how often each earlier prefix value occurred.
from typing import List, Optional, Any
from collections import defaultdict


def countSubarraysWithSum(numbers: List[int], target: int) -> int:
    seen = defaultdict(int)
    seen[0] = 1
    running = 0
    total = 0
    for value in numbers:
        running += value
        total += seen[running - target]
        seen[running] += 1
    return total

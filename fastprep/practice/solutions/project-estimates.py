# Hash-set lookup: for each distinct value, check whether value + target exists.
from typing import List, Optional, Any


def countPairs(n: int, projectCosts: List[int], target: int) -> int:
    seen = set(projectCosts)
    count = 0
    for v in seen:
        if v + target in seen:
            count += 1
    return count

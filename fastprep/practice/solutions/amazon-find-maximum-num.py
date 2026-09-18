# Greedy: sort the per-subject remaining deficits ascending and take the cheapest ones first.
from typing import List, Optional, Any


def findMaximumNum(answered: List[int], needed: List[int], q: int) -> int:
    deficits = sorted(max(0, n - a) for a, n in zip(answered, needed))
    passed = 0
    budget = q
    for d in deficits:
        if d > budget:
            break
        budget -= d
        passed += 1
    return passed

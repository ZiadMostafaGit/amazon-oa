# Approach: single pass with a Counter, then emit values whose count > 1 in first-occurrence order.
from typing import List, Optional, Any
from collections import Counter


def findDuplicateValues(data: List[int]) -> List[int]:
    counts = Counter(data)
    seen = set()
    result = []
    for value in data:
        if counts[value] > 1 and value not in seen:
            seen.add(value)
            result.append(value)
    return result

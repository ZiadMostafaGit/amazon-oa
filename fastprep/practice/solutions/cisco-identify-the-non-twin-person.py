# Count occurrences; a person is un-paired when its count is odd, so take the smallest such value.
from typing import List, Optional, Any
from collections import Counter


def identifyNonTwinPerson(inputArr: List[int]) -> int:
    counts = Counter(inputArr)
    odd = [v for v, c in counts.items() if c % 2 == 1]
    return min(odd) if odd else -1

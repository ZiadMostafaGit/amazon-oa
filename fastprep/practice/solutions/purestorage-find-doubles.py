# Counting map: keep every x whose double occurs exactly once in the list.
from typing import List
from collections import Counter


def findDoubles(numbers: List[int]) -> List[int]:
    freq = Counter(numbers)
    result = [x for x in numbers if freq.get(2 * x, 0) == 1]
    result.sort()
    return result

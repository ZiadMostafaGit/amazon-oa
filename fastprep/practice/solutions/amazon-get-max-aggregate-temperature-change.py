# Prefix and suffix running sums; the answer is the largest value either scan reaches.
from typing import List, Optional, Any


def getMaxAggregateTemperatureChange(tempChange: List[int]) -> int:
    best = None
    run = 0
    for v in tempChange:
        run += v
        if best is None or run > best:
            best = run
    run = 0
    for v in reversed(tempChange):
        run += v
        if run > best:
            best = run
    return best

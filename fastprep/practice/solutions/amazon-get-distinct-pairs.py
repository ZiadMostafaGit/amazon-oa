# Hash-set counting of distinct value pairs summing to the target.
from typing import List, Optional, Any
from collections import Counter


def getDistinctPairs(stocksProfit: List[int], target: int) -> int:
    counts = Counter(stocksProfit)
    total = 0
    for value, freq in counts.items():
        other = target - value
        if other < value:
            continue
        if other == value:
            if freq >= 2:
                total += 1
        elif other in counts:
            total += 1
    return total

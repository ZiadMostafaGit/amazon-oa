# House-robber DP over distinct sorted values (taking v forbids v-1 and v+1).
from collections import Counter
from typing import List, Optional, Any


def maxEscapeGameScore(elements: List[int]) -> int:
    if not elements:
        return 0
    counts = Counter(elements)
    values = sorted(counts)
    skip = 0          # best score not using the previous value
    take = 0          # best score considering up to the previous value
    prev = None
    for value in values:
        gain = value * counts[value]
        if prev is not None and value == prev + 1:
            skip, take = take, max(take, skip + gain)
        else:
            skip, take = take, take + gain
        prev = value
    return take

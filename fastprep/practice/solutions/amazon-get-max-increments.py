# Greedy/counting: interleaving the most frequent value optimally leaves n - maxFrequency ascents.
from typing import List, Optional, Any
from collections import Counter


def getMaxIncrements(scores: List[int]) -> int:
    if not scores:
        return 0
    return len(scores) - max(Counter(scores).values())

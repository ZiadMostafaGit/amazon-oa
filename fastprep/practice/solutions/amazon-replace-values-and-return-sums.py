# Keep value -> count and the running sum; replacing old by new moves count[old] copies at once. O(n + q).
from typing import List, Optional, Any
from collections import Counter


def replaceValuesAndReturnSums(entries: List[int], transactions: List[List[int]]) -> List[int]:
    count = Counter(entries)
    total = sum(entries)
    out = []
    for old, new in transactions:
        c = count.get(old, 0)
        if c and old != new:
            total += (new - old) * c
            del count[old]
            count[new] += c
        out.append(total)
    return out

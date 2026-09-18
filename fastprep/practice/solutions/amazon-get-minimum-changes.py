# Equal length-k window sums force period k; per residue class keep the most frequent value.
from collections import Counter
from typing import List


def getMinimumChanges(prod_price: List[int], k: int) -> int:
    n = len(prod_price)
    groups = [Counter() for _ in range(k)]
    for i, v in enumerate(prod_price):
        groups[i % k][v] += 1
    kept = 0
    for c in groups:
        if c:
            kept += max(c.values())
    return n - kept

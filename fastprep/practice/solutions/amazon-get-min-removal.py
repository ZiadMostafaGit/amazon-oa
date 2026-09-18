# Count categories, keep the k most frequent ones, remove everything else.
from collections import Counter
from typing import List


def getminRemoval(catalogue: List[int], k: int) -> int:
    counts = sorted(Counter(catalogue).values(), reverse=True)
    return len(catalogue) - sum(counts[:k])

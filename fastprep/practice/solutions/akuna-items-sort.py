# Approach: counting map, then sort by (frequency, value).
from typing import List, Optional, Any
from collections import Counter


def itemsSort(items: List[int]) -> List[int]:
    freq = Counter(items)
    return sorted(items, key=lambda x: (freq[x], x))

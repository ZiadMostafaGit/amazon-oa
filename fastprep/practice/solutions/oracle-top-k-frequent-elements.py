# Count with a hash map, then sort distinct values by (-frequency, -value) and take the first k.
from typing import List, Optional, Any
from collections import Counter


def topKFrequent(nums: List[int], k: int) -> List[int]:
    freq = Counter(nums)
    order = sorted(freq.keys(), key=lambda v: (-freq[v], -v))
    return order[:k]

# Frequency map, then buckets indexed by frequency (0..n); read buckets from high to low. O(n log n) only for tie order inside a bucket.
from typing import List, Optional, Any
from collections import Counter


def topKFrequent(nums: List[int], k: int) -> List[int]:
    freq = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for value, f in freq.items():
        buckets[f].append(value)
    out = []
    for f in range(len(nums), 0, -1):
        for value in sorted(buckets[f]):
            out.append(value)
            if len(out) == k:
                return out
    return out

# Per-partition local top-k counts merged into a global top-k by (-freq, value).
from typing import List, Optional, Any
import heapq
from collections import Counter


def topKFrequentByPartition(partitions: List[List[int]], k: int) -> List[int]:
    candidates = []
    for part in partitions:
        counts = Counter(part)
        # local top k of this partition (values are disjoint across partitions)
        local = heapq.nsmallest(k, counts.items(), key=lambda kv: (-kv[1], kv[0]))
        candidates.extend(local)
    best = heapq.nsmallest(k, candidates, key=lambda kv: (-kv[1], kv[0]))
    return [v for v, _ in best]

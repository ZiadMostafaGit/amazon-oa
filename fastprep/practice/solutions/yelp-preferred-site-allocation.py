# Bucket customers per site, then sort each bucket by (-priority, index) and take the top capacity[s].
from typing import List, Optional, Any


def allocatePreferredSites(preferredSite: List[int], priority: List[int], capacity: List[int]) -> List[int]:
    n = len(preferredSite)
    result = [-1] * n
    buckets = [[] for _ in range(len(capacity))]
    for i in range(n):
        buckets[preferredSite[i]].append(i)

    for s, members in enumerate(buckets):
        cap = capacity[s]
        if cap <= 0 or not members:
            continue
        members.sort(key=lambda i: (-priority[i], i))
        for i in members[:cap]:
            result[i] = s
    return result

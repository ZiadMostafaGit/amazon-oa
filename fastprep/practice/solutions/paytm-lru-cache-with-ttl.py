# OrderedDict for LRU recency plus a lazy-deletion min-heap of expiry times for TTL purging.
import heapq
from collections import OrderedDict
from typing import List, Optional, Any


def cacheResults(capacity: int, ttl: int, operations: List[List[int]]) -> List[int]:
    cache: "OrderedDict[int, List[int]]" = OrderedDict()  # key -> [value, expiry]
    expiry_heap: List[Any] = []  # (expiry, key)
    results: List[int] = []

    for op in operations:
        typ, t, key, value = op[0], op[1], op[2], op[3]

        # purge everything whose expiry time has been reached
        while expiry_heap and expiry_heap[0][0] <= t:
            exp, k = heapq.heappop(expiry_heap)
            entry = cache.get(k)
            if entry is not None and entry[1] == exp:
                del cache[k]

        if typ == 0:
            new_expiry = t + ttl
            if key in cache:
                entry = cache[key]
                entry[0] = value
                entry[1] = new_expiry
                cache.move_to_end(key)
            else:
                if len(cache) >= capacity:
                    cache.popitem(last=False)
                cache[key] = [value, new_expiry]
            heapq.heappush(expiry_heap, (new_expiry, key))
        else:
            entry = cache.get(key)
            if entry is None:
                results.append(-1)
            else:
                cache.move_to_end(key)
                results.append(entry[0])

    return results

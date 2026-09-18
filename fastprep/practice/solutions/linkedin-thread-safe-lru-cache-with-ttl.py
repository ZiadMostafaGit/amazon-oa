# Ordered-dict LRU cache plus a min-heap of expirations to lazily purge TTL-expired keys.
from typing import List, Optional, Any
import heapq
from collections import OrderedDict


def runLRUWithTTL(capacity: int, operations: List[str], arguments: List[List[int]]) -> List[str]:
    cache = OrderedDict()   # key -> value, most recent at the end
    expiry = {}             # key -> current expiration time
    heap = []               # (expire_time, key) lazily validated
    out = []

    def purge(now: int) -> None:
        while heap and heap[0][0] <= now:
            exp, key = heapq.heappop(heap)
            if key in expiry and expiry[key] == exp:
                del expiry[key]
                cache.pop(key, None)

    for op, args in zip(operations, arguments):
        if op == "PUT":
            time, key, value, ttl = args[0], args[1], args[2], args[3]
            purge(time)
            if capacity <= 0:
                out.append("null")
                continue
            if key in cache:
                cache[key] = value
                cache.move_to_end(key)
            else:
                if len(cache) >= capacity:
                    old, _ = cache.popitem(last=False)
                    expiry.pop(old, None)
                cache[key] = value
            exp = time + ttl
            expiry[key] = exp
            heapq.heappush(heap, (exp, key))
            out.append("null")
        else:
            time, key = args[0], args[1]
            purge(time)
            if key in cache:
                cache.move_to_end(key)
                out.append(str(cache[key]))
            else:
                out.append("-1")
    return out

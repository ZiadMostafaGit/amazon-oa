# Hash map plus two lazy-deletion heaps: one ordered by expiration, one by (age, key) for eviction.
import heapq
from typing import List, Optional, Any


def runCapacityTimedCache(capacity: int, operations: List[List[int]]) -> List[int]:
    entries = {}          # key -> [value, expire, age, ver]
    exp_heap = []         # (expire, key, ver)
    age_heap = []         # (age, key, ver)
    ver = 0
    out = []

    def purge(now: int) -> None:
        while exp_heap and exp_heap[0][0] <= now:
            e, k, v = heapq.heappop(exp_heap)
            cur = entries.get(k)
            if cur is not None and cur[3] == v:
                del entries[k]

    for op in operations:
        if op[0] == 1:
            key, ts = op[1], op[2]
            purge(ts)
            cur = entries.get(key)
            out.append(cur[0] if cur is not None else -1)
        else:
            key, value, ttl, ts = op[1], op[2], op[3], op[4]
            purge(ts)
            if key not in entries and len(entries) >= capacity:
                while age_heap:
                    a, k, v = heapq.heappop(age_heap)
                    cur = entries.get(k)
                    if cur is not None and cur[3] == v:
                        del entries[k]
                        break
            ver += 1
            expire = ts + ttl
            entries[key] = [value, expire, ts, ver]
            heapq.heappush(exp_heap, (expire, key, ver))
            heapq.heappush(age_heap, (ts, key, ver))
    return out

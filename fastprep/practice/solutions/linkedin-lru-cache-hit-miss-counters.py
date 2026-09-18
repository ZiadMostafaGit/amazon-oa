# OrderedDict LRU simulation with integer half-up rounding for the hit rate.
from typing import List, Optional, Any
from collections import OrderedDict


def runLruWithCounters(capacity: int, operations: List[str]) -> List[str]:
    cache = OrderedDict()
    out = []
    hits = 0
    misses = 0
    for op in operations:
        parts = op.split()
        if not parts:
            continue
        if parts[0] == "PUT":
            key = parts[1]
            value = parts[2] if len(parts) > 2 else ""
            if key in cache:
                cache.move_to_end(key)
                cache[key] = value
            else:
                cache[key] = value
                if len(cache) > capacity:
                    cache.popitem(last=False)
        else:
            key = parts[1]
            if key in cache:
                cache.move_to_end(key)
                hits += 1
                out.append("HIT " + cache[key])
            else:
                misses += 1
                out.append("MISS")
    gets = hits + misses
    if gets == 0:
        rate = 0
    else:
        rate = (hits * 2000 + gets) // (2 * gets)
    out.append("STATS %d %d %d.%03d" % (hits, misses, rate // 1000, rate % 1000))
    return out

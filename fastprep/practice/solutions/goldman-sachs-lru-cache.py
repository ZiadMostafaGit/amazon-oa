# Ordered dictionary as an LRU cache: move_to_end on access, popitem(last=False) to evict.
from typing import List, Optional, Any
from collections import OrderedDict


def runLRU(capacity: int, operations: List[str]) -> List[int]:
    cache: "OrderedDict[int, int]" = OrderedDict()
    results: List[int] = []
    for op in operations:
        parts = op.split()
        if parts[0] == "GET":
            key = int(parts[1])
            if key in cache:
                cache.move_to_end(key)
                results.append(cache[key])
            else:
                results.append(-1)
        else:
            key = int(parts[1])
            value = int(parts[2])
            if key in cache:
                cache[key] = value
                cache.move_to_end(key)
            else:
                if len(cache) >= capacity:
                    cache.popitem(last=False)
                cache[key] = value
    return results

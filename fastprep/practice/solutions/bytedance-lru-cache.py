# OrderedDict as a hash map plus recency list: O(1) per GET/PUT.
from collections import OrderedDict
from typing import List, Optional, Any


def runLRU(capacity: int, operations: List[str]) -> List[int]:
    cache = OrderedDict()
    results = []
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

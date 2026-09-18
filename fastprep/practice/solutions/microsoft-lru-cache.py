# OrderedDict as an LRU: move_to_end on hit/update, popitem(last=False) to evict.
from collections import OrderedDict
from typing import List, Optional, Any


def runLRU(capacity: int, operations: List[str]) -> List[int]:
    cache = OrderedDict()
    out = []
    for op in operations:
        parts = op.split()
        if parts[0] == 'PUT':
            key = int(parts[1])
            val = int(parts[2])
            if key in cache:
                cache.move_to_end(key)
            cache[key] = val
            if len(cache) > capacity:
                cache.popitem(last=False)
        else:
            key = int(parts[1])
            if key in cache:
                cache.move_to_end(key)
                out.append(cache[key])
            else:
                out.append(-1)
    return out

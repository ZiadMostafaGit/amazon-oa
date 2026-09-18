# OrderedDict as an LRU cache: move_to_end on hit/update, popitem(last=False) to evict.
from collections import OrderedDict
from typing import List, Optional, Any


def runLRU(capacity: int, operations: List[str]) -> List[int]:
    cache = OrderedDict()
    out = []
    for op in operations:
        parts = op.split()
        if not parts:
            continue
        kind = parts[0].upper()
        if kind == "GET":
            key = int(parts[1])
            if key in cache:
                cache.move_to_end(key)
                out.append(cache[key])
            else:
                out.append(-1)
        else:  # PUT
            key = int(parts[1])
            value = int(parts[2])
            if key in cache:
                cache[key] = value
                cache.move_to_end(key)
            else:
                if len(cache) >= capacity:
                    cache.popitem(last=False)
                cache[key] = value
    return out

# LRU cache backed by an OrderedDict with move_to_end / popitem(last=False) eviction.
from typing import List, Optional, Any
from collections import OrderedDict


def runLRU(capacity: int, operations: List[str]) -> List[int]:
    cache: "OrderedDict[int, int]" = OrderedDict()
    out: List[int] = []
    for op in operations:
        parts = op.split()
        kind = parts[0]
        if kind == "PUT":
            key = int(parts[1])
            value = int(parts[2])
            if key in cache:
                cache[key] = value
                cache.move_to_end(key)
            else:
                if len(cache) >= capacity:
                    cache.popitem(last=False)
                cache[key] = value
        else:
            key = int(parts[1])
            if key in cache:
                out.append(cache[key])
                cache.move_to_end(key)
            else:
                out.append(-1)
    return out

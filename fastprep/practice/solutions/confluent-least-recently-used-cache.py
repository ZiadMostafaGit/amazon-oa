# LRU cache backed by an OrderedDict: move_to_end on hit/update, popitem(last=False) to evict.
from typing import List, Optional, Any
from collections import OrderedDict


def runLRU(capacity: int, operations: List[str]) -> List[int]:
    cache: "OrderedDict[int, int]" = OrderedDict()
    out: List[int] = []
    for op in operations:
        parts = op.split()
        cmd = parts[0].upper()
        key = int(parts[1])
        if cmd == "GET":
            if key in cache:
                cache.move_to_end(key)
                out.append(cache[key])
            else:
                out.append(-1)
        else:
            value = int(parts[2])
            if key in cache:
                cache[key] = value
                cache.move_to_end(key)
            else:
                if len(cache) >= capacity:
                    cache.popitem(last=False)
                cache[key] = value
    return out

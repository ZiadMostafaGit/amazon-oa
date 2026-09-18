# LRU cache backed by an OrderedDict: move_to_end on access, popitem(last=False) to evict.
from collections import OrderedDict
from typing import List


def runQueryCache(capacity: int, operations: List[List[int]]) -> List[str]:
    cache = OrderedDict()
    out = []
    for op in operations:
        if op[0] == 1:
            key = op[1]
            if key in cache:
                cache.move_to_end(key)
                out.append(str(cache[key]))
            else:
                out.append("-1")
        else:
            key, value = op[1], op[2]
            if key in cache:
                cache.move_to_end(key)
            cache[key] = value
            if len(cache) > capacity:
                cache.popitem(last=False)
            out.append("null")
    return out

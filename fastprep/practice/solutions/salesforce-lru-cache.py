# OrderedDict-backed LRU cache replaying the operation batch in order.
from typing import List, Optional, Any
from collections import OrderedDict


def runLruCache(capacity: int, operations: List[str], arguments: List[List[int]]) -> List[int]:
    cache = OrderedDict()
    out = []
    for op, args in zip(operations, arguments):
        if op == "get":
            key = args[0]
            if key in cache:
                cache.move_to_end(key)
                out.append(cache[key])
            else:
                out.append(-1)
        else:
            key, value = args[0], args[1]
            if key in cache:
                cache.move_to_end(key)
            cache[key] = value
            if len(cache) > capacity:
                cache.popitem(last=False)
    return out

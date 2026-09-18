# LRU via OrderedDict: move_to_end on access/update, popitem(last=False) to evict.
from typing import List, Optional, Any
from collections import OrderedDict


def processLruVariation(capacity: int, operations: List[str], arguments: List[List[int]]) -> List[int]:
    cache = OrderedDict()
    result = []

    for op, args in zip(operations, arguments):
        if op == "get":
            key = args[0]
            if key in cache:
                cache.move_to_end(key)
                result.append(cache[key])
            else:
                result.append(-1)
        else:
            key, value = args[0], args[1]
            if key in cache:
                cache[key] = value
                cache.move_to_end(key)
            else:
                if len(cache) >= capacity:
                    cache.popitem(last=False)
                cache[key] = value
    return result

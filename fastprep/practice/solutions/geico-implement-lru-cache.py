# Parse the op log and replay it against an OrderedDict-backed LRU cache, emitting one line per get.
from typing import List, Optional, Any
from collections import OrderedDict


def solveLRUCacheOperations(input: str) -> List[str]:
    capacity = 0
    cache = OrderedDict()
    out = []
    for raw in input.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("capacity"):
            capacity = int(line.split("=", 1)[1].strip())
            cache = OrderedDict()
            continue
        name, _, rest = line.partition("(")
        name = name.strip()
        args = rest.rstrip().rstrip(")")
        parts = [p.strip() for p in args.split(",") if p.strip() != ""]
        if name == "put":
            key, value = int(parts[0]), int(parts[1])
            if key in cache:
                cache.move_to_end(key)
            cache[key] = value
            while capacity > 0 and len(cache) > capacity:
                cache.popitem(last=False)
        elif name == "get":
            key = int(parts[0])
            if key in cache:
                cache.move_to_end(key)
                out.append(str(cache[key]))
            else:
                out.append("-1")
    return out

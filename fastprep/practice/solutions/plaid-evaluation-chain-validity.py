# Iterative chain walk with memoized resolution and on-path marking for cycle detection.
from typing import List, Optional, Any


def evaluateChains(links: List[List[str]]) -> List[str]:
    invalid = ["INVALID"]
    defs = {}
    for row in links:
        name, target = row[0], row[1]
        if name in defs:
            return invalid          # duplicate definition
        defs[name] = target

    resolved = {}                   # name -> bool
    on_path = set()

    for start in defs:
        if start in resolved:
            continue
        path = []
        cur = start
        value = None
        while True:
            if cur in resolved:
                value = resolved[cur]
                break
            low = cur.lower()
            if low == "true" or low == "false":
                value = (low == "true")
                break
            if cur not in defs:
                return invalid      # dangling reference
            if cur in on_path:
                return invalid      # cycle
            on_path.add(cur)
            path.append(cur)
            cur = defs[cur]
        for name in path:
            resolved[name] = value
            on_path.discard(name)

    return ["%s:%s" % (name, "true" if resolved[name] else "false")
            for name in sorted(defs)]

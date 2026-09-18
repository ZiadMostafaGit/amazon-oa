# Sort the products once, then binary search each accumulated prefix and take up to three.
from bisect import bisect_left
from typing import List, Optional, Any


def searchSuggestions(products: List[str], query: str) -> List[List[str]]:
    items = sorted(products)
    result = []
    prefix = ""
    dead = False
    for ch in query:
        prefix += ch
        if dead:
            result.append([])
            continue
        start = bisect_left(items, prefix)
        matches = []
        idx = start
        while idx < len(items) and len(matches) < 3 and items[idx].startswith(prefix):
            matches.append(items[idx])
            idx += 1
        if not matches:
            dead = True
        result.append(matches)
    return result

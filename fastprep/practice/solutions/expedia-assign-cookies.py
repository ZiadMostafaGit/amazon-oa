from typing import List, Optional, Any


def assignCookies(greed: List[int], cookies: List[int]) -> int:
    g = sorted(greed)
    c = sorted(cookies)
    i = 0
    for size in c:
        if i < len(g) and size >= g[i]:
            i += 1
    return i

# DP over prefixes: reachable[i] is true when s[:i] splits into dictionary words; only distinct word lengths are tried.
from typing import List, Optional, Any


def wordBreak(s: str, dictionary: List[str]) -> bool:
    n = len(s)
    if n == 0:
        return True
    words = set(dictionary)
    lengths = sorted({len(w) for w in words if 0 < len(w) <= n})
    if not lengths:
        return False
    reachable = [False] * (n + 1)
    reachable[0] = True
    for i in range(1, n + 1):
        for L in lengths:
            if L > i:
                break
            if reachable[i - L] and s[i - L:i] in words:
                reachable[i] = True
                break
    return reachable[n]

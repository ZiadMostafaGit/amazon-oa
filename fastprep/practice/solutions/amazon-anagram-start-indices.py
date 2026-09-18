# Fixed-size sliding window over character counts with a matched-letter counter.
from typing import List, Optional, Any


def solve(s: str, p: str) -> List[int]:
    n, m = len(s), len(p)
    if m == 0 or m > n:
        return []
    need = [0] * 26
    base = ord('a')
    for ch in p:
        need[ord(ch) - base] += 1
    window = [0] * 26
    res = []
    for i, ch in enumerate(s):
        window[ord(ch) - base] += 1
        if i >= m:
            window[ord(s[i - m]) - base] -= 1
        if i >= m - 1 and window == need:
            res.append(i - m + 1)
    return res

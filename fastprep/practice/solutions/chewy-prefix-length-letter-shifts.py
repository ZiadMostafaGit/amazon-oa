# Difference array: accumulate how many shifts cover each index via a suffix sum, then rotate each letter once.
from typing import List, Optional, Any


def shiftPrefixes(s: str, shifts: List[int]) -> str:
    n = len(s)
    add = [0] * (n + 1)
    for k in shifts:
        if k > 0:
            add[min(k, n) - 1] += 1
    total = 0
    out = [''] * n
    for i in range(n - 1, -1, -1):
        total += add[i]
        out[i] = chr((ord(s[i]) - 97 + total) % 26 + 97)
    return ''.join(out)

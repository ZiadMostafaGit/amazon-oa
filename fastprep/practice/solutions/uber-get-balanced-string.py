from typing import List, Optional, Any


def getBalancedString(arr: List[int]) -> str:
    n = len(arr)
    pos = [0] * (n + 1)
    for i, v in enumerate(arr):
        pos[v] = i
    out = []
    lo = hi = pos[1]
    for k in range(1, n + 1):
        lo = min(lo, pos[k])
        hi = max(hi, pos[k])
        # values 1..k fill a window exactly when their span has length k
        out.append('1' if hi - lo + 1 == k else '0')
    return "".join(out)

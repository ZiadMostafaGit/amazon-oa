# Difference array: count how many rolls cover each prefix position, then shift.
from typing import List, Optional, Any


def rollTheString(s: str, roll: List[int]) -> str:
    n = len(s)
    diff = [0] * (n + 1)
    for r in roll:
        if r > 0:
            diff[0] += 1
            diff[min(r, n)] -= 1
    out = []
    cur = 0
    for i in range(n):
        cur += diff[i]
        out.append(chr((ord(s[i]) - 97 + cur) % 26 + 97))
    return "".join(out)

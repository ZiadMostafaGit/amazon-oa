# Count ordered index pairs by splitting the access code string at every position and multiplying fragment-string counts.
from collections import Counter
from typing import List, Optional, Any


def countAccessCodePairs(fragments: List[int], accessCode: int) -> int:
    s = str(accessCode)
    counts = Counter(str(f) for f in fragments)
    total = 0
    for p in range(1, len(s)):
        pre, suf = s[:p], s[p:]
        a = counts.get(pre, 0)
        b = counts.get(suf, 0)
        if a == 0 or b == 0:
            continue
        if pre == suf:
            total += a * (a - 1)
        else:
            total += a * b
    return total

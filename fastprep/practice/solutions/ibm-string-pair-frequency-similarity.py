# Per-pair letter frequency counting, comparing each of the 26 counts.
from typing import List, Optional, Any
from collections import Counter


def areSimilar(s: List[str], t: List[str]) -> List[str]:
    out = []
    for a, b in zip(s, t):
        ca, cb = Counter(a), Counter(b)
        ok = True
        for ch in set(ca) | set(cb):
            if abs(ca[ch] - cb[ch]) > 3:
                ok = False
                break
        out.append("YES" if ok else "NO")
    return out

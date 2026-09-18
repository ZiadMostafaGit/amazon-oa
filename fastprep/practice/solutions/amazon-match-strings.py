# Wildcard with exactly one '*': check prefix and suffix around the star, no overlap.
from typing import List, Optional, Any


def matchStrings(text: List[str], pat: List[str]) -> List[str]:
    res = []
    for s, p in zip(text, pat):
        k = p.index("*")
        pre = p[:k]
        suf = p[k + 1:]
        if len(pre) + len(suf) > len(s):
            res.append("NO")
            continue
        ok = s.startswith(pre) and (suf == "" or s.endswith(suf))
        res.append("YES" if ok else "NO")
    return res

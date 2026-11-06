# Group by a 26-entry letter-count vector (no sorting of characters), then
# order each group and the groups canonically.
from typing import List, Optional, Any


def solve(strs: List[str]) -> List[List[str]]:
    buckets = {}
    for s in strs:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1
        buckets.setdefault(tuple(cnt), []).append(s)
    groups = [sorted(g) for g in buckets.values()]
    groups.sort(key=lambda g: g[0])
    return groups

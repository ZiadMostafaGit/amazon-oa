# Hash strings by sorted-character key, then sort within and across groups.
from typing import List, Optional, Any


def groupAnagrams(strs: List[str]) -> List[List[str]]:
    buckets = {}
    for s in strs:
        key = "".join(sorted(s))
        buckets.setdefault(key, []).append(s)
    groups = [sorted(g) for g in buckets.values()]
    groups.sort(key=lambda g: g[0])
    return groups

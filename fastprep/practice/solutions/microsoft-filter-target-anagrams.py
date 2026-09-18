# Approach: compare sorted-character signatures (O(1) length prefilter) of each word against the target.
from typing import List, Optional, Any
from collections import Counter


def filterTargetAnagrams(words: List[str], target: str) -> List[str]:
    n = len(target)
    key = Counter(target)
    out = []
    for w in words:
        if len(w) == n and Counter(w) == key:
            out.append(w)
    return out

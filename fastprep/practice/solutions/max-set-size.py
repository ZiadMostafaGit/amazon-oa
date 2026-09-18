# Hash set plus chain walking: start at every value that has no square-root predecessor
# and follow v -> v*v while the next value is present, tracking the longest chain.
from typing import List, Optional, Any


def maxSetSize(riceBags: List[int]) -> int:
    present = set(riceBags)
    best = 0
    for v in present:
        root = int(v ** 0.5)
        # fix floating point drift around the integer square root
        while root * root > v:
            root -= 1
        while (root + 1) * (root + 1) <= v:
            root += 1
        if root * root == v and root in present:
            continue  # not the start of a chain
        length = 1
        cur = v
        while cur * cur in present:
            cur *= cur
            length += 1
        if length > best:
            best = length
    return best if best >= 2 else -1

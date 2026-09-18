# House-robber DP: rolling take/skip maxima over the jars.
from typing import List, Optional, Any


def maximumChocolates(jars: List[int]) -> int:
    prev, cur = 0, 0
    for v in jars:
        prev, cur = cur, max(cur, prev + v)
    return cur

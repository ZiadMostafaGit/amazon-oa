# Mark every ancestor of p, then climb from q until a marked node appears.
from typing import List, Optional, Any


def lowestCommonAncestor(parent: List[int], p: int, q: int) -> int:
    seen = set()
    while p != -1:
        seen.add(p)
        p = parent[p]
    while q not in seen:
        q = parent[q]
    return q

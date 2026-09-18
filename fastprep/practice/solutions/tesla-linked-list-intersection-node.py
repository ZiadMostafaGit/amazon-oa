# Mark every node index on list A, then walk list B until a marked index appears.
from typing import List, Optional, Any


def findIntersectionNodeIndex(nodes: List[List[int]], headA: int, headB: int) -> int:
    seen = set()
    cur = headA
    while cur != -1 and cur not in seen:
        seen.add(cur)
        cur = nodes[cur][1]
    cur = headB
    visited = set()
    while cur != -1 and cur not in visited:
        if cur in seen:
            return cur
        visited.add(cur)
        cur = nodes[cur][1]
    return -1

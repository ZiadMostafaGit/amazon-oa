# Mark every node reachable from headA, then walk from headB until a marked node appears.
from typing import List, Optional, Any


def findIntersectionNode(next: List[int], headA: int, headB: int) -> int:
    n = len(next)
    if headA < 0 or headB < 0 or n == 0:
        return -1
    seen = bytearray(n)
    cur = headA
    while cur != -1:
        seen[cur] = 1
        cur = next[cur]
    cur = headB
    while cur != -1:
        if seen[cur]:
            return cur
        cur = next[cur]
    return -1

# Keep a count per server id and a running total; each day move a whole bucket in O(1).
from collections import Counter
from typing import List, Optional, Any


def getTotalRequests(server: List[int], replaced: List[int], newId: List[int]) -> List[int]:
    count = Counter(server)
    total = sum(i * c for i, c in count.items())
    out = []
    for j in range(len(replaced)):
        old, new = replaced[j], newId[j]
        c = count.get(old, 0)
        if c and old != new:
            del count[old]
            total -= old * c
            count[new] = count.get(new, 0) + c
            total += new * c
        out.append(total)
    return out

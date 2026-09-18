# Sorted list of obstacle coordinates with binary search (bisect) per query.
from typing import List, Optional, Any
import bisect


def obstaclePlacementQueries(operations: List[List[int]]) -> str:
    obstacles: List[int] = []
    out: List[str] = []
    for op in operations:
        if op[0] == 1:
            x = op[1]
            bisect.insort(obstacles, x)
        else:
            x = op[1]
            size = op[2]
            # block occupies [x - size, x - 1]
            idx = bisect.bisect_left(obstacles, x)
            if idx > 0 and obstacles[idx - 1] >= x - size:
                out.append('0')
            else:
                out.append('1')
    return ''.join(out)

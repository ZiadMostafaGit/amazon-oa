# Circle traversal: skip the single largest arc gap, so answer = total_servers - maxGap.
from typing import List


def getMinTime(total_servers: int, servers: List[int]) -> int:
    pts = sorted(set(servers))
    m = len(pts)
    if m <= 1:
        return 0
    max_gap = pts[0] + total_servers - pts[-1]  # wrap-around arc
    for i in range(1, m):
        gap = pts[i] - pts[i - 1]
        if gap > max_gap:
            max_gap = gap
    return total_servers - max_gap

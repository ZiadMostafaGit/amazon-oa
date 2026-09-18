# Bitset transitive closure (Floyd-Warshall over Python big-int bitmasks).
from typing import List


def answerReachabilityQueries(n: int, edges: List[List[int]], queries: List[List[int]]) -> List[bool]:
    reach = [1 << i for i in range(n)]
    for u, v in edges:
        reach[u] |= 1 << v
    for k in range(n):
        bit = 1 << k
        for i in range(n):
            if reach[i] & bit:
                reach[i] |= reach[k]
    return [bool(reach[s] >> t & 1) for s, t in queries]

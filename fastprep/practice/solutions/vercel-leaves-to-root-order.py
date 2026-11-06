from typing import List, Optional, Any


def leavesToRoots(n: int, edges: List[List[int]]) -> List[int]:
    parents = [[] for _ in range(n)]
    outdeg = [0] * n
    for p, c in edges:
        parents[c].append(p)
        outdeg[p] += 1
    order = []
    layer = [i for i in range(n) if outdeg[i] == 0]
    while layer:
        order.extend(layer)
        nxt = []
        for c in layer:
            for p in parents[c]:
                outdeg[p] -= 1
                if outdeg[p] == 0:
                    nxt.append(p)
        layer = sorted(nxt)
    return order if len(order) == n else []

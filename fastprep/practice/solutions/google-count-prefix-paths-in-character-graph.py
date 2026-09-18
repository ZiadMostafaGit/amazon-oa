# Bitmask DP over (visited set, last vertex) extended one target character at a time.
from typing import List, Optional, Any


def countPrefixPaths(labels: str, edges: List[List[int]], target: str) -> List[int]:
    n = len(labels)
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u

    m = len(target)
    counts = [0] * m

    # states: dict keyed by (mask, last) -> path count
    cur = {}
    c0 = target[0]
    for i in range(n):
        if labels[i] == c0:
            cur[(1 << i, i)] = cur.get((1 << i, i), 0) + 1
    counts[0] = sum(cur.values())

    for k in range(1, m):
        ch = target[k]
        nxt = {}
        for (mask, last), cnt in cur.items():
            avail = adj[last] & ~mask
            while avail:
                b = avail & (-avail)
                avail ^= b
                j = b.bit_length() - 1
                if labels[j] != ch:
                    continue
                key = (mask | b, j)
                nxt[key] = nxt.get(key, 0) + cnt
        cur = nxt
        counts[k] = sum(cur.values())
        if not cur:
            break
    return counts

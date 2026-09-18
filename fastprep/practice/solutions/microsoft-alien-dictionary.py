# Kahn topological sort over adjacent-word precedence edges, using a min-heap for the smallest order.
from typing import List, Optional, Any
import heapq


def alienOrder(words: List[str]) -> str:
    chars = set()
    for w in words:
        chars.update(w)
    adj = {c: set() for c in chars}
    indeg = {c: 0 for c in chars}

    for i in range(len(words) - 1):
        a, b = words[i], words[i + 1]
        m = min(len(a), len(b))
        j = 0
        while j < m and a[j] == b[j]:
            j += 1
        if j == m:
            if len(a) > len(b):
                return ""
            continue
        if b[j] not in adj[a[j]]:
            adj[a[j]].add(b[j])
            indeg[b[j]] += 1

    heap = [c for c in chars if indeg[c] == 0]
    heapq.heapify(heap)
    out = []
    while heap:
        c = heapq.heappop(heap)
        out.append(c)
        for nxt in sorted(adj[c]):
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)
    if len(out) != len(chars):
        return ""
    return "".join(out)

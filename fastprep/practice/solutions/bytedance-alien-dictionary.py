# Kahn topological sort over letter precedence edges, using a min-heap for the smallest valid order.
import heapq
from typing import List


def alienOrder(words: List[str]) -> str:
    adj = {}
    indeg = {}
    for w in words:
        for ch in w:
            adj.setdefault(ch, set())
            indeg.setdefault(ch, 0)

    for i in range(len(words) - 1):
        a, b = words[i], words[i + 1]
        found = False
        for x, y in zip(a, b):
            if x != y:
                if y not in adj[x]:
                    adj[x].add(y)
                    indeg[y] += 1
                found = True
                break
        if not found and len(a) > len(b):
            return ""

    heap = [c for c in indeg if indeg[c] == 0]
    heapq.heapify(heap)
    out = []
    while heap:
        c = heapq.heappop(heap)
        out.append(c)
        for nxt in adj[c]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)
    if len(out) != len(indeg):
        return ""
    return "".join(out)

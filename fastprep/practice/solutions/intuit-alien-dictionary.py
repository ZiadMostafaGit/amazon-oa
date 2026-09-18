# Kahn topological sort with a min-heap to get the lexicographically smallest order.
import heapq
from typing import List


def alienOrder(words: List[str]) -> str:
    letters = set()
    for w in words:
        letters.update(w)
    adj = {c: set() for c in letters}
    indeg = {c: 0 for c in letters}
    for a, b in zip(words, words[1:]):
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
    heap = [c for c in letters if indeg[c] == 0]
    heapq.heapify(heap)
    out = []
    while heap:
        c = heapq.heappop(heap)
        out.append(c)
        for nxt in adj[c]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)
    if len(out) != len(letters):
        return ""
    return "".join(out)

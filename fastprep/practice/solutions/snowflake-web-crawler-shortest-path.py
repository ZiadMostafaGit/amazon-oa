# Reverse BFS for distances to the target, then a greedy forward walk picking the smallest name each step.
from typing import List, Optional, Any
from collections import deque


def shortestPagePath(pages: List[str], links: List[List[str]], start: str, target: str) -> List[str]:
    if start == target:
        return [start]
    out = {p: [] for p in pages}
    rev = {p: [] for p in pages}
    for a, b in links:
        out.setdefault(a, []).append(b)
        rev.setdefault(b, []).append(a)

    # distance from each page to target, over reversed edges
    dist = {target: 0}
    q = deque([target])
    while q:
        v = q.popleft()
        for u in rev.get(v, ()):
            if u not in dist:
                dist[u] = dist[v] + 1
                q.append(u)

    if start not in dist:
        return []

    path = [start]
    cur = start
    while cur != target:
        need = dist[cur] - 1
        best = None
        for nxt in out.get(cur, ()):
            if dist.get(nxt, -1) == need and (best is None or nxt < best):
                best = nxt
        path.append(best)
        cur = best
    return path

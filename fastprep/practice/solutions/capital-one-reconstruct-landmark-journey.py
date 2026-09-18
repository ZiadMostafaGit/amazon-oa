# Treat photos as a path graph: start at an endpoint (degree 1) and walk the adjacency list.
from typing import List, Optional, Any


def solution(travelPhotos: List[List[int]]) -> List[int]:
    adj = {}
    order = []  # landmarks in order of first appearance, used as a deterministic tie-break
    for a, b in travelPhotos:
        for x in (a, b):
            if x not in adj:
                adj[x] = []
                order.append(x)
        adj[a].append(b)
        adj[b].append(a)

    if not adj:
        return []

    start = None
    for node in order:
        if len(adj[node]) == 1:
            start = node
            break
    if start is None:
        start = order[0]

    journey = [start]
    prev = None
    cur = start
    while True:
        nxt = None
        for nb in adj[cur]:
            if nb != prev:
                nxt = nb
                break
        if nxt is None or len(journey) == len(adj):
            break
        journey.append(nxt)
        prev, cur = cur, nxt
    return journey

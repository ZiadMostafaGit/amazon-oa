# Approach: build a bidirectional weighted graph (edge and its reciprocal) and BFS for the product.
from collections import deque
from typing import List, Optional, Any


def solve(rates: List[List[str]], query: List[str]) -> str:
    graph = {}
    for row in rates:
        if len(row) < 3:
            continue
        src, dst, val = row[0], row[1], float(row[2])
        graph.setdefault(src, []).append((dst, val))
        graph.setdefault(dst, [])
        if val != 0:
            graph[dst].append((src, 1.0 / val))

    if len(query) < 2:
        return "-1.00"
    start, end = query[0], query[1]
    if start not in graph or end not in graph:
        return "-1.00"
    if start == end:
        return "%.2f" % 1.0

    seen = {start}
    dq = deque([(start, 1.0)])
    while dq:
        node, acc = dq.popleft()
        for nxt, w in graph.get(node, []):
            if nxt in seen:
                continue
            product = acc * w
            if nxt == end:
                return "%.2f" % product
            seen.add(nxt)
            dq.append((nxt, product))
    return "-1.00"

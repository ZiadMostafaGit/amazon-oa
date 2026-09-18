# Greedy per center: take the center's value plus its top-k positive neighbour values.
from typing import List, Optional, Any


def getMaximumSumKStar(g_nodes: int, g_from: List[int], g_to: List[int], values: List[int], k: int) -> int:
    adj = [[] for _ in range(g_nodes + 1)]
    for a, b in zip(g_from, g_to):
        adj[a].append(values[b - 1])
        adj[b].append(values[a - 1])

    best = None
    for node in range(1, g_nodes + 1):
        total = values[node - 1]
        if k > 0 and adj[node]:
            arms = sorted(adj[node], reverse=True)[:k]
            for v in arms:
                if v <= 0:
                    break
                total += v
        if best is None or total > best:
            best = total
    return best if best is not None else 0

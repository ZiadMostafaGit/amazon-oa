from typing import List, Optional, Any


def maxCatScore(costs: List[List[int]], scores: List[List[int]], budget: int) -> int:
    # grouped knapsack: best[b] = max score using spend at most b
    best = [0] * (budget + 1)
    for cs, ss in zip(costs, scores):
        nxt = best[:]  # this cat stays still
        for c, s in zip(cs, ss):
            for b in range(c, budget + 1):
                v = best[b - c] + s
                if v > nxt[b]:
                    nxt[b] = v
        best = nxt
    return best[budget]

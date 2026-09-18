# Bigram counting with an incrementally maintained best successor per token.
from typing import List, Optional, Any


def predictNextWords(trainingTokens: List[str], queries: List[str]) -> List[str]:
    counts = {}  # token -> {successor: count}
    best = {}    # token -> (best successor, its count)

    for i in range(len(trainingTokens) - 1):
        a = trainingTokens[i]
        b = trainingTokens[i + 1]
        bucket = counts.get(a)
        if bucket is None:
            bucket = {}
            counts[a] = bucket
        c = bucket.get(b, 0) + 1
        bucket[b] = c
        cur = best.get(a)
        if cur is None or c > cur[1] or (c == cur[1] and b < cur[0]):
            best[a] = (b, c)

    out = []
    for q in queries:
        cur = best.get(q)
        out.append(cur[0] if cur is not None else "")
    return out

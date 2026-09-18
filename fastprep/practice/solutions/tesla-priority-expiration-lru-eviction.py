# Single linear scan keeping the best candidate under a lexicographic tie-break key.
from typing import List, Optional, Any


def selectEvictionKey(keys: List[int], priorities: List[int], expirations: List[int], lastUsed: List[int], now: int) -> int:
    expired_best = None
    for i, k in enumerate(keys):
        if expirations[i] <= now:
            if expired_best is None or k < expired_best:
                expired_best = k
    if expired_best is not None:
        return expired_best

    best = None
    best_rank = None
    for i, k in enumerate(keys):
        rank = (priorities[i], lastUsed[i], k)
        if best_rank is None or rank < best_rank:
            best_rank = rank
            best = k
    return best

# Length-bounded DP over reachable partial sums (offset array), summing hits on target.
from typing import List, Optional, Any


def countOrderedCombinationSumsWithNegatives(candidates: List[int], target: int, maxLength: int) -> int:
    if not candidates or maxLength < 1:
        return 0
    limit = maxLength * max(abs(c) for c in candidates)
    if abs(target) > limit:
        return 0
    size = 2 * limit + 1
    off = limit
    cur = [0] * size
    cur[off] = 1  # empty sequence, sum 0
    answer = 0
    for _ in range(maxLength):
        nxt = [0] * size
        for s in range(size):
            ways = cur[s]
            if not ways:
                continue
            for c in candidates:
                j = s + c
                if 0 <= j < size:
                    nxt[j] += ways
        answer += nxt[target + off]
        cur = nxt
    return answer

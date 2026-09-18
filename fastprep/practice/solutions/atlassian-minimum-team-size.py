# Sliding window: the minimal covering end index is monotonic in the start index.
from typing import List, Optional, Any


def teamSize(talent: List[int], talentsCount: int) -> List[int]:
    n = len(talent)
    counts = [0] * (talentsCount + 2)
    distinct = 0
    right = 0
    ans = [-1] * n
    for i in range(n):
        while distinct < talentsCount and right < n:
            t = talent[right]
            counts[t] += 1
            if counts[t] == 1:
                distinct += 1
            right += 1
        if distinct < talentsCount:
            break
        ans[i] = right - i
        t = talent[i]
        counts[t] -= 1
        if counts[t] == 0:
            distinct -= 1
    return ans

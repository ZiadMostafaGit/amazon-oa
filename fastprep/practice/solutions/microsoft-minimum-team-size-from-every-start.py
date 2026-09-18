# Sliding window with two pointers: the minimal covering end index is monotone in the start.
from typing import List, Optional, Any


def minimumTeamSizes(talent: List[int], talentsCount: int) -> List[int]:
    n = len(talent)
    count = [0] * (talentsCount + 2)
    distinct = 0
    j = 0
    ans = [-1] * n
    for i in range(n):
        while distinct < talentsCount and j < n:
            t = talent[j]
            if t <= talentsCount:
                if count[t] == 0:
                    distinct += 1
                count[t] += 1
            j += 1
        if distinct == talentsCount:
            ans[i] = j - i
        else:
            ans[i] = -1
        t = talent[i]
        if t <= talentsCount:
            count[t] -= 1
            if count[t] == 0:
                distinct -= 1
    return ans

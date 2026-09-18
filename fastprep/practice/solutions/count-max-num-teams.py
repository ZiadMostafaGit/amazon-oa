# Sort, then greedily take the leftmost feasible block of teamSize consecutive skills.
from typing import List, Optional, Any


def countMaxNumTeams(skill: List[int], teamSize: int, maxDiff: int) -> int:
    s = sorted(skill)
    n = len(s)
    count = 0
    i = 0
    while i + teamSize - 1 < n:
        if s[i + teamSize - 1] - s[i] <= maxDiff:
            count += 1
            i += teamSize
        else:
            i += 1
    return count

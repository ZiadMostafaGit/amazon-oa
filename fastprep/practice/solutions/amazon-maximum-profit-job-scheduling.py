# Sort jobs by end time, DP over prefix best with binary search for the last compatible job.
from bisect import bisect_right
from typing import List, Optional, Any


def solve(startTime: List[int], endTime: List[int], profit: List[int]) -> int:
    jobs = sorted(zip(endTime, startTime, profit))
    ends = [0]
    best = [0]
    for e, s, p in jobs:
        idx = bisect_right(ends, s) - 1
        cand = best[idx] + p
        if cand > best[-1]:
            ends.append(e)
            best.append(cand)
        else:
            ends.append(e)
            best.append(best[-1])
    return best[-1]

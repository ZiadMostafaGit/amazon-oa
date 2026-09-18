# Offline sweep over time with a Fenwick tree counting skills bucketed by their most recent request time.
from typing import List, Optional, Any


def getStaleSkillCount(numSkills: int, requestLogs: List[List[int]], queryTimes: List[int], timeWindow: int) -> List[int]:
    maxT = 0
    for _, ts in requestLogs:
        if ts > maxT:
            maxT = ts
    for q in queryTimes:
        if q > maxT:
            maxT = q

    size = maxT + 2
    tree = [0] * (size + 1)

    def add(i, delta):
        i += 1
        while i <= size:
            tree[i] += delta
            i += i & (-i)

    def pref(i):
        i += 1
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        return s

    logsByTime = [[] for _ in range(maxT + 1)]
    for skill, ts in requestLogs:
        if ts <= maxT:
            logsByTime[ts].append(skill)

    queriesByTime = [[] for _ in range(maxT + 1)]
    for idx, q in enumerate(queryTimes):
        queriesByTime[q].append(idx)

    last = [-1] * (numSkills + 1)
    answer = [0] * len(queryTimes)

    for t in range(maxT + 1):
        for skill in logsByTime[t]:
            prev = last[skill]
            if prev == t:
                continue
            if prev >= 0:
                add(prev, -1)
            last[skill] = t
            add(t, 1)
        for idx in queriesByTime[t]:
            lo = t - timeWindow
            if lo < 0:
                lo = 0
            active = pref(t) - (pref(lo - 1) if lo > 0 else 0)
            answer[idx] = numSkills - active

    return answer

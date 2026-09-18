# Approach: timestamp each point-assignment, then apply the suffix-maximum of later global floors.
from typing import List, Optional, Any


def findPodCount(pods: List[int], logs: List[List[int]]) -> List[int]:
    n = len(pods)
    m = len(logs)
    # last_time[i]: index in logs of the last direct assignment to i (-1 = initial value)
    last_time = [-1] * n
    value = list(pods)
    # floor_at[t]: the global floor applied by logs[t], or 0 if logs[t] is not a floor op
    floor_at = [0] * m

    for t, log in enumerate(logs):
        op = log[0]
        if op == 1:
            p = log[1] - 1
            value[p] = log[2]
            last_time[p] = t
        else:
            floor_at[t] = log[2]

    # suffix_floor[t] = max floor among logs[t..m-1]
    suffix_floor = [0] * (m + 1)
    for t in range(m - 1, -1, -1):
        suffix_floor[t] = suffix_floor[t + 1]
        if floor_at[t] > suffix_floor[t]:
            suffix_floor[t] = floor_at[t]

    result = []
    for i in range(n):
        # floors strictly after the last assignment to i still apply
        start = last_time[i] + 1
        result.append(max(value[i], suffix_floor[start]))
    return result

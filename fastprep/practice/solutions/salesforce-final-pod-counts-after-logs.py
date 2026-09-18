# Lazy floors: suffix maximum of the type-2 thresholds applied at each service's last direct set time.
from typing import List, Optional, Any


def getFinalPods(pods: List[int], logs: List[List[int]]) -> List[int]:
    n = len(pods)
    m = len(logs)
    NEG = float("-inf")
    # suf[j] = max threshold among type-2 logs at index >= j
    suf = [NEG] * (m + 1)
    for j in range(m - 1, -1, -1):
        s = suf[j + 1]
        if logs[j][0] == 2 and logs[j][2] > s:
            s = logs[j][2]
        suf[j] = s

    res = list(pods)
    last_set = [-1] * n  # log index of the last type-1 log touching this service
    for j in range(m):
        log = logs[j]
        if log[0] == 1:
            p = log[1] - 1
            if 0 <= p < n:
                res[p] = log[2]
                last_set[p] = j

    for i in range(n):
        start = last_set[i] + 1  # floors that happened after the last direct set
        floor = suf[start]
        if floor != NEG and floor > res[i]:
            res[i] = int(floor)
    return res

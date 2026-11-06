# Permute the four digits with a used array, skipping equal digits at the same depth, and keep valid HH:MM.
from typing import List, Optional, Any


def enumerateValidTimes(digits: List[int]) -> List[str]:
    d = sorted(digits)
    used = [False] * len(d)
    cur = []
    out = []

    def go():
        if len(cur) == 4:
            h = cur[0] * 10 + cur[1]
            m = cur[2] * 10 + cur[3]
            if h <= 23 and m <= 59:
                out.append("%02d:%02d" % (h, m))
            return
        for i in range(len(d)):
            if used[i] or (i > 0 and d[i] == d[i - 1] and not used[i - 1]):
                continue
            used[i] = True
            cur.append(d[i])
            go()
            cur.pop()
            used[i] = False

    go()
    return out  # sorted digits => permutations come out in increasing order, i.e. chronological

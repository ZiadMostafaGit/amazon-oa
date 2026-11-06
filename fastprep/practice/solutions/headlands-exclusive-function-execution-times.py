# Call stack: the top is the running function; charge it the time since the last event.
from typing import List


def getTotalExecutionTime(n: int, logs: List[str]) -> List[int]:
    res = [0] * n
    stack = []
    prev = 0  # start of the next uncharged second
    for log in logs:
        fid, kind, ts = log.split(':')
        fid, ts = int(fid), int(ts)
        if kind == 'start':
            if stack:
                res[stack[-1]] += ts - prev
            stack.append(fid)
            prev = ts
        else:
            res[stack.pop()] += ts - prev + 1
            prev = ts + 1
    return res

# Version-interval log per (key, field): each write stores [start, end, value); queries scan intervals.
from typing import List, Optional, Any


def historicalFieldValues(operations: List[List[str]]) -> List[str]:
    INF = float('inf')
    # (key, field) -> list of [start, end, value_str]
    hist = {}
    out = []

    def close_current(rec, t):
        # end any version still live at time t
        if rec:
            last = rec[-1]
            if last[1] > t:
                last[1] = t

    for op in operations:
        name = op[0]
        if name == "SET":
            t = int(op[1])
            key, field, value, ttl = op[2], op[3], op[4], int(op[5])
            rec = hist.setdefault((key, field), [])
            close_current(rec, t)
            end = t + ttl if ttl > 0 else INF
            rec.append([t, end, value])
        elif name == "DELETE":
            t = int(op[1])
            key, field = op[2], op[3]
            rec = hist.get((key, field))
            if rec:
                close_current(rec, t)
        else:
            t = int(op[1])
            key, field = op[2], op[3]
            at = int(op[4]) if name == "GET_WHEN" else t
            rec = hist.get((key, field), [])
            found = "NULL"
            for start, end, value in rec:
                if start <= at < end:
                    found = value
                    break
                if start > at:
                    break
            out.append(found)
    return out

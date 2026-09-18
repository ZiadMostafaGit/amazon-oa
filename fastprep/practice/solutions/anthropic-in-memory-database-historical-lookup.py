# Versioned history per (key, field) with binary search over strictly increasing write timestamps.
from typing import List, Optional, Any
from bisect import bisect_right

INF = float('inf')


def inMemoryDatabaseHistoricalLookup(operations: List[List[str]]) -> List[str]:
    # history[(key, field)] = (starts, entries) where entries[i] = (start, value_or_None, expire)
    history = {}
    out = []

    def visible(kf, t):
        rec = history.get(kf)
        if not rec:
            return None
        starts, entries = rec
        i = bisect_right(starts, t) - 1
        if i < 0:
            return None
        start, value, expire = entries[i]
        if value is None:
            return None
        end = expire
        if i + 1 < len(starts):
            end = min(end, starts[i + 1])
        if t < end:
            return value
        return None

    def append(kf, start, value, expire):
        rec = history.get(kf)
        if rec is None:
            rec = ([], [])
            history[kf] = rec
        rec[0].append(start)
        rec[1].append((start, value, expire))

    for op in operations:
        name = op[0]
        if name == "SET_AT":
            key, field, value, ts = op[1], op[2], op[3], int(op[4])
            append((key, field), ts, value, INF)
            out.append("")
        elif name == "SET_AT_WITH_TTL":
            key, field, value, ts, ttl = op[1], op[2], op[3], int(op[4]), int(op[5])
            append((key, field), ts, value, ts + ttl)
            out.append("")
        elif name == "DELETE_AT":
            key, field, ts = op[1], op[2], int(op[3])
            if visible((key, field), ts) is not None:
                append((key, field), ts, None, INF)
                out.append("true")
            else:
                out.append("false")
        elif name == "GET_WHEN":
            ts = int(op[1])
            key, field = op[2], op[3]
            at = int(op[4])
            if at == 0:
                at = ts
            v = visible((key, field), at)
            out.append("null" if v is None else v)
        else:
            out.append("")
    return out

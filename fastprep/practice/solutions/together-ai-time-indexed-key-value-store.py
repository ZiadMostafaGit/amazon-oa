# Per-key sorted timestamp list maintained with bisect; GET is a binary search for the predecessor.
from bisect import bisect_left, bisect_right
from typing import List, Optional, Any


def timeMap(operations: List[List[str]]) -> List[str]:
    times = {}
    vals = {}
    out = []

    for op in operations:
        kind = op[0]
        if kind == "SET":
            key, ts, value = op[1], int(op[2]), op[3]
            ta = times.setdefault(key, [])
            va = vals.setdefault(key, [])
            i = bisect_left(ta, ts)
            if i < len(ta) and ta[i] == ts:
                va[i] = value
            else:
                ta.insert(i, ts)
                va.insert(i, value)
        else:
            key, ts = op[1], int(op[2])
            ta = times.get(key)
            if not ta:
                out.append("")
                continue
            i = bisect_right(ta, ts) - 1
            out.append(vals[key][i] if i >= 0 else "")
    return out

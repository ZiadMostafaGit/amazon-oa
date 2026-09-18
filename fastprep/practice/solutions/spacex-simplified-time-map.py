# Per-key append-only timestamp lists (already sorted) with binary search for each get.
from bisect import bisect_right
from typing import List, Optional, Any


def timeMapResults(operations: List[List[str]]) -> List[str]:
    times = {}
    vals = {}
    out = []
    for op in operations:
        if op[0] == "set":
            key, value, ts = op[1], op[2], int(op[3])
            if key not in times:
                times[key] = []
                vals[key] = []
            times[key].append(ts)
            vals[key].append(value)
        else:
            key, ts = op[1], int(op[2])
            arr = times.get(key)
            if not arr:
                out.append("")
                continue
            i = bisect_right(arr, ts)
            out.append(vals[key][i - 1] if i else "")
    return out

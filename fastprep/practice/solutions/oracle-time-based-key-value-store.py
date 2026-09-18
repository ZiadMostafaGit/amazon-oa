# Per-key append-only timestamp list with binary search (bisect) for each get.
from typing import List, Optional, Any
from bisect import bisect_right


def runTimeMap(operations: List[str], keys: List[str], values: List[str], timestamps: List[int]) -> List[str]:
    times = {}
    vals = {}
    out = []
    for i, op in enumerate(operations):
        key = keys[i]
        ts = timestamps[i]
        if op == "set":
            if key not in times:
                times[key] = []
                vals[key] = []
            tl = times[key]
            vl = vals[key]
            # timestamps per key are strictly increasing, so append keeps order
            if tl and ts <= tl[-1]:
                pos = bisect_right(tl, ts)
                tl.insert(pos, ts)
                vl.insert(pos, values[i])
            else:
                tl.append(ts)
                vl.append(values[i])
            out.append("null")
        else:
            tl = times.get(key)
            if not tl:
                out.append("")
                continue
            pos = bisect_right(tl, ts)
            out.append(vals[key][pos - 1] if pos else "")
    return out

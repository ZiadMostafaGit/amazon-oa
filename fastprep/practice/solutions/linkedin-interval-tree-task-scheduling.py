# Keep accepted disjoint bookings sorted by start; binary search for overlap and range queries.
import bisect
from typing import List, Optional, Any


def scheduleTasks(operations: List[str]) -> List[str]:
    starts: List[int] = []
    ends: List[int] = []
    ids: List[str] = []
    out: List[str] = []
    for op in operations:
        parts = op.split()
        kind = parts[0]
        if kind == "BOOK":
            bid = parts[1]
            s = int(parts[2])
            e = int(parts[3])
            i = bisect.bisect_left(starts, s)
            ok = True
            if i > 0 and ends[i - 1] > s:
                ok = False
            if ok and i < len(starts) and starts[i] < e:
                ok = False
            if ok:
                starts.insert(i, s)
                ends.insert(i, e)
                ids.insert(i, bid)
                out.append("true")
            else:
                out.append("false")
        else:
            qs = int(parts[1])
            qe = int(parts[2])
            hits: List[str] = []
            i = bisect.bisect_left(starts, qs)
            if i > 0 and ends[i - 1] > qs:
                i -= 1
            while i < len(starts) and starts[i] < qe:
                if ends[i] > qs:
                    hits.append(ids[i])
                i += 1
            out.append(",".join(hits))
    return out

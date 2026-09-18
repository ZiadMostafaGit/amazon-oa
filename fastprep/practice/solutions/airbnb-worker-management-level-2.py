# Simulation with hash maps plus a sort by (-total, id) for the TOP_N_WORKERS query.
from typing import List, Optional, Any


def workerManagementLevel2(operations: List[List[str]]) -> List[str]:
    position_of = {}
    open_entry = {}
    total = {}
    out = []

    for op in operations:
        kind = op[0]
        if kind == "ADD_WORKER":
            wid, position = op[1], op[2]
            if wid in position_of:
                out.append("false")
            else:
                position_of[wid] = position
                total[wid] = 0
                out.append("true")
        elif kind == "REGISTER":
            wid, ts = op[1], int(op[2])
            if wid not in position_of:
                out.append("invalid_request")
            else:
                if wid in open_entry:
                    total[wid] += ts - open_entry.pop(wid)
                else:
                    open_entry[wid] = ts
                out.append("registered")
        elif kind == "GET":
            wid = op[1]
            out.append("" if wid not in position_of else str(total[wid]))
        elif kind == "TOP_N_WORKERS":
            n, position = int(op[1]), op[2]
            cands = [w for w, p in position_of.items() if p == position]
            cands.sort(key=lambda w: (-total[w], w))
            out.append(", ".join("%s(%d)" % (w, total[w]) for w in cands[:n]))
        else:
            out.append("")
    return out

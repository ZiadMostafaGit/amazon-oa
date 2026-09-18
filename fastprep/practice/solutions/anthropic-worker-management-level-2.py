# Approach: same session-toggling registry as part 1, plus a sort by (-total, worker id) filtered by position.
from typing import List, Optional, Any


def workerManagementLevel2(operations: List[List[str]]) -> List[str]:
    workers = {}
    out: List[str] = []
    for op in operations:
        kind = op[0]
        if kind == "ADD_WORKER":
            wid, position, comp = op[1], op[2], op[3]
            if wid in workers:
                out.append("false")
            else:
                workers[wid] = {
                    "position": position,
                    "compensation": comp,
                    "entry": None,
                    "total": 0,
                }
                out.append("true")
        elif kind == "REGISTER":
            wid, ts = op[1], int(op[2])
            w = workers.get(wid)
            if w is None:
                out.append("invalid_request")
            else:
                if w["entry"] is None:
                    w["entry"] = ts
                else:
                    w["total"] += ts - w["entry"]
                    w["entry"] = None
                out.append("registered")
        elif kind == "GET":
            w = workers.get(op[1])
            out.append("" if w is None else str(w["total"]))
        elif kind == "TOP_N_WORKERS":
            n, position = int(op[1]), op[2]
            cands = [(w["total"], wid) for wid, w in workers.items() if w["position"] == position]
            cands.sort(key=lambda t: (-t[0], t[1]))
            out.append(", ".join("%s(%d)" % (wid, total) for total, wid in cands[:n]))
        else:
            out.append("")
    return out

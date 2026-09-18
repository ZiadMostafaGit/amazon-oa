# Approach: dict of worker records; toggle entry/exit state on REGISTER and accumulate completed session lengths.
from typing import List, Optional, Any


def workerManagementLevel1(operations: List[List[str]]) -> List[str]:
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
            wid = op[1]
            w = workers.get(wid)
            out.append("" if w is None else str(w["total"]))
        else:
            out.append("")
    return out

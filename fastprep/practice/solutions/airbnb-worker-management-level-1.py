# Simulation with a hash map of worker records and an open-session timestamp per worker.
from typing import List, Optional, Any


def workerManagementLevel1(operations: List[List[str]]) -> List[str]:
    info = {}          # worker_id -> (position, compensation)
    open_entry = {}    # worker_id -> timestamp of an unfinished entry
    total = {}         # worker_id -> total completed time
    out = []

    for op in operations:
        kind = op[0]
        if kind == "ADD_WORKER":
            wid, position, compensation = op[1], op[2], op[3]
            if wid in info:
                out.append("false")
            else:
                info[wid] = (position, compensation)
                total[wid] = 0
                out.append("true")
        elif kind == "REGISTER":
            wid, ts = op[1], int(op[2])
            if wid not in info:
                out.append("invalid_request")
            else:
                if wid in open_entry:
                    total[wid] += ts - open_entry.pop(wid)
                else:
                    open_entry[wid] = ts
                out.append("registered")
        elif kind == "GET":
            wid = op[1]
            out.append("" if wid not in info else str(total[wid]))
        else:
            out.append("")
    return out

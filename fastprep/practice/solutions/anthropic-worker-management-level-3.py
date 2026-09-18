# Approach: stateful registry storing completed sessions with the position/compensation active at entry;
# a pending promotion applies on the next entry at or after its start timestamp.
from typing import List, Optional, Any


def workerManagementLevel3(operations: List[List[str]]) -> List[str]:
    workers = {}
    out: List[str] = []
    for op in operations:
        kind = op[0]
        if kind == "ADD_WORKER":
            wid, position, comp = op[1], op[2], int(op[3])
            if wid in workers:
                out.append("false")
            else:
                workers[wid] = {
                    "position": position,
                    "comp": comp,
                    "entry": None,
                    "entry_position": None,
                    "entry_comp": None,
                    "sessions": [],
                    "pending": None,
                }
                out.append("true")
        elif kind == "REGISTER":
            wid, ts = op[1], int(op[2])
            w = workers.get(wid)
            if w is None:
                out.append("invalid_request")
            else:
                if w["entry"] is None:
                    pend = w["pending"]
                    if pend is not None and ts >= pend[2]:
                        w["position"] = pend[0]
                        w["comp"] = pend[1]
                        w["pending"] = None
                    w["entry"] = ts
                    w["entry_position"] = w["position"]
                    w["entry_comp"] = w["comp"]
                else:
                    w["sessions"].append(
                        (w["entry"], ts, w["entry_comp"], w["entry_position"])
                    )
                    w["entry"] = None
                out.append("registered")
        elif kind == "GET":
            w = workers.get(op[1])
            if w is None:
                out.append("")
            else:
                out.append(str(sum(e - s for s, e, _c, _p in w["sessions"])))
        elif kind == "TOP_N_WORKERS":
            n, position = int(op[1]), op[2]
            cands = []
            for wid, w in workers.items():
                if w["position"] != position:
                    continue
                total = sum(e - s for s, e, _c, p in w["sessions"] if p == position)
                cands.append((total, wid))
            cands.sort(key=lambda t: (-t[0], t[1]))
            out.append(", ".join("%s(%d)" % (wid, total) for total, wid in cands[:n]))
        elif kind == "PROMOTE":
            wid, new_position, new_comp, start = op[1], op[2], int(op[3]), int(op[4])
            w = workers.get(wid)
            if w is None or w["pending"] is not None:
                out.append("invalid_request")
            else:
                w["pending"] = (new_position, new_comp, start)
                out.append("success")
        elif kind == "CALC_SALARY":
            wid, lo, hi = op[1], int(op[2]), int(op[3])
            w = workers.get(wid)
            if w is None:
                out.append("")
            else:
                total = 0
                for s, e, c, _p in w["sessions"]:
                    a = max(s, lo)
                    b = min(e, hi)
                    if b > a:
                        total += (b - a) * c
                out.append(str(total))
        else:
            out.append("")
    return out

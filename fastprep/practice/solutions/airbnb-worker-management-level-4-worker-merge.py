# Simulation: per-worker session log carrying its own compensation and overtime rule; merge splices session logs.
from typing import List, Optional, Any, Dict


def workerManagementLevel4WorkerMerge(operations: List[List[str]]) -> List[str]:
    workers: Dict[str, dict] = {}
    out: List[str] = []

    def session_salary(start: int, end: int, comp: int, thr: Optional[int],
                       lo: int, hi: int) -> int:
        a = start if start > lo else lo
        b = end if end < hi else hi
        if b <= a:
            return 0
        # offsets measured from the session start
        oa, ob = a - start, b - start
        if thr is None:
            return (ob - oa) * comp
        reg_hi = thr if thr < ob else ob
        reg = reg_hi - oa
        if reg < 0:
            reg = 0
        over = (ob - oa) - reg
        return reg * comp + over * 2 * comp

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
                    "entry_comp": None,
                    "entry_rule": None,
                    "rule": None,
                    "total": 0,
                    "sessions": [],
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
                    w["entry_comp"] = w["comp"]
                    w["entry_rule"] = w["rule"]
                else:
                    start = w["entry"]
                    w["total"] += ts - start
                    w["sessions"].append((start, ts, w["entry_comp"], w["entry_rule"]))
                    w["entry"] = None
                    w["entry_comp"] = None
                    w["entry_rule"] = None
                out.append("registered")
        elif kind == "GET":
            w = workers.get(op[1])
            out.append("" if w is None else str(w["total"]))
        elif kind == "TOP_N_WORKERS":
            n, position = int(op[1]), op[2]
            cands = [(-w["total"], wid) for wid, w in workers.items()
                     if w["position"] == position]
            cands.sort()
            out.append(", ".join("%s(%d)" % (wid, -t) for t, wid in cands[:n]))
        elif kind == "SET_OVERTIME_RULE":
            wid, thr = op[1], int(op[2])
            w = workers.get(wid)
            if w is None:
                out.append("invalid_request")
            else:
                w["rule"] = thr
                out.append("success")
        elif kind == "CALC_SALARY":
            wid, lo, hi = op[1], int(op[2]), int(op[3])
            w = workers.get(wid)
            if w is None:
                out.append("")
            else:
                salary = 0
                for s, e, comp, thr in w["sessions"]:
                    salary += session_salary(s, e, comp, thr, lo, hi)
                out.append(str(salary))
        elif kind == "MERGE_WORKERS":
            a, b = op[1], op[2]
            wa, wb = workers.get(a), workers.get(b)
            if wa is None or wb is None or a == b \
                    or wa["entry"] is not None or wb["entry"] is not None:
                out.append("invalid_request")
            else:
                wa["sessions"].extend(wb["sessions"])
                wa["total"] += wb["total"]
                del workers[b]
                out.append("success")
        else:
            out.append("")
    return out

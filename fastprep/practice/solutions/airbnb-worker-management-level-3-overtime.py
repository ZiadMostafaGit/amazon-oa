# Simulation: store each completed session with the rate and overtime threshold fixed at its entry.
from typing import List, Optional, Any


def workerManagementLevel3Overtime(operations: List[List[str]]) -> List[str]:
    position_of = {}
    rate_of = {}
    pending_threshold = {}   # latest rule set so far (applies to the next entry)
    open_entry = {}          # wid -> (start_ts, threshold_at_entry)
    sessions = {}            # wid -> list of (start, end, rate, threshold)
    total = {}
    out = []

    for op in operations:
        kind = op[0]
        if kind == "ADD_WORKER":
            wid, position, comp = op[1], op[2], int(op[3])
            if wid in position_of:
                out.append("false")
            else:
                position_of[wid] = position
                rate_of[wid] = comp
                total[wid] = 0
                sessions[wid] = []
                out.append("true")
        elif kind == "REGISTER":
            wid, ts = op[1], int(op[2])
            if wid not in position_of:
                out.append("invalid_request")
            else:
                if wid in open_entry:
                    start, th = open_entry.pop(wid)
                    sessions[wid].append((start, ts, rate_of[wid], th))
                    total[wid] += ts - start
                else:
                    open_entry[wid] = (ts, pending_threshold.get(wid))
                out.append("registered")
        elif kind == "GET":
            wid = op[1]
            out.append("" if wid not in position_of else str(total[wid]))
        elif kind == "SET_OVERTIME_RULE":
            wid, threshold = op[1], int(op[2])
            if wid not in position_of:
                out.append("invalid_request")
            else:
                pending_threshold[wid] = threshold
                out.append("success")
        elif kind == "CALC_SALARY":
            wid, qs, qe = op[1], int(op[2]), int(op[3])
            if wid not in position_of:
                out.append("")
            else:
                salary = 0
                for start, end, rate, th in sessions[wid]:
                    lo = max(start, qs)
                    hi = min(end, qe)
                    if hi <= lo:
                        continue
                    a = lo - start
                    b = hi - start
                    if th is None:
                        regular = b - a
                    else:
                        regular = max(0, min(b, th) - a)
                    overtime = (b - a) - regular
                    salary += regular * rate + overtime * 2 * rate
                out.append(str(salary))
        elif kind == "TOP_N_WORKERS":
            n, position = int(op[1]), op[2]
            cands = [w for w, p in position_of.items() if p == position]
            cands.sort(key=lambda w: (-total[w], w))
            out.append(", ".join("%s(%d)" % (w, total[w]) for w in cands[:n]))
        else:
            out.append("")
    return out

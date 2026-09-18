# Simulation: pending promotion applied at the next qualifying entry; sessions stamped with position+rate.
from typing import List, Optional, Any


def workerManagementLevel3(operations: List[List[str]]) -> List[str]:
    position_of = {}
    rate_of = {}
    pending = {}        # wid -> (new_position, new_rate, start_ts)
    open_entry = {}     # wid -> (start_ts, position, rate)
    sessions = {}       # wid -> list of (start, end, rate)
    total = {}          # wid -> total completed time over all positions
    by_position = {}    # wid -> {position: completed time}
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
                by_position[wid] = {}
                out.append("true")
        elif kind == "REGISTER":
            wid, ts = op[1], int(op[2])
            if wid not in position_of:
                out.append("invalid_request")
            else:
                if wid in open_entry:
                    start, pos, rate = open_entry.pop(wid)
                    sessions[wid].append((start, ts, rate))
                    dur = ts - start
                    total[wid] += dur
                    by_position[wid][pos] = by_position[wid].get(pos, 0) + dur
                else:
                    promo = pending.get(wid)
                    if promo is not None and ts >= promo[2]:
                        position_of[wid] = promo[0]
                        rate_of[wid] = promo[1]
                        del pending[wid]
                    open_entry[wid] = (ts, position_of[wid], rate_of[wid])
                out.append("registered")
        elif kind == "PROMOTE":
            wid, new_pos, new_comp, start_ts = op[1], op[2], int(op[3]), int(op[4])
            if wid not in position_of or wid in pending:
                out.append("invalid_request")
            else:
                pending[wid] = (new_pos, new_comp, start_ts)
                out.append("success")
        elif kind == "CALC_SALARY":
            wid, qs, qe = op[1], int(op[2]), int(op[3])
            if wid not in position_of:
                out.append("")
            else:
                salary = 0
                for start, end, rate in sessions[wid]:
                    lo = max(start, qs)
                    hi = min(end, qe)
                    if hi > lo:
                        salary += (hi - lo) * rate
                out.append(str(salary))
        elif kind == "GET":
            wid = op[1]
            out.append("" if wid not in position_of else str(total[wid]))
        elif kind == "TOP_N_WORKERS":
            n, position = int(op[1]), op[2]
            cands = [w for w, p in position_of.items() if p == position]
            cands.sort(key=lambda w: (-by_position[w].get(position, 0), w))
            out.append(", ".join("%s(%d)" % (w, by_position[w].get(position, 0)) for w in cands[:n]))
        else:
            out.append("")
    return out

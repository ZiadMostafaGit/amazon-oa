# Simulation: per-worker sessions with entry-time position/pay, plus merged grant intervals per salary query.
import bisect
from typing import List, Optional, Any


def workerManagementFullShiftGrants(operations: List[List[str]]) -> List[str]:
    workers = {}
    grants = []
    results = []

    def merged():
        if not grants:
            return [], []
        ivs = sorted(grants)
        starts = []
        ends = []
        cs, ce = ivs[0]
        for s, e in ivs[1:]:
            if s <= ce:
                if e > ce:
                    ce = e
            else:
                starts.append(cs)
                ends.append(ce)
                cs, ce = s, e
        starts.append(cs)
        ends.append(ce)
        return starts, ends

    for op in operations:
        name = op[0]
        if name == "ADD_WORKER":
            wid, pos, comp = op[1], op[2], int(op[3])
            if wid in workers:
                results.append("false")
            else:
                workers[wid] = {
                    "pos": pos,
                    "comp": comp,
                    "pending": None,
                    "open": None,
                    "sessions": [],
                }
                results.append("true")
        elif name == "REGISTER":
            wid, ts = op[1], int(op[2])
            w = workers.get(wid)
            if w is None:
                results.append("invalid_request")
            else:
                if w["open"] is None:
                    pend = w["pending"]
                    if pend is not None and ts >= pend[2]:
                        w["pos"] = pend[0]
                        w["comp"] = pend[1]
                        w["pending"] = None
                    w["open"] = (ts, w["pos"], w["comp"])
                else:
                    st, pos, comp = w["open"]
                    w["sessions"].append((st, ts, pos, comp))
                    w["open"] = None
                results.append("registered")
        elif name == "GET":
            w = workers.get(op[1])
            if w is None:
                results.append("")
            else:
                results.append(str(sum(e - s for s, e, _, _ in w["sessions"])))
        elif name == "TOP_N_WORKERS":
            n, pos = int(op[1]), op[2]
            rows = []
            for wid, w in workers.items():
                if w["pos"] == pos:
                    t = sum(e - s for s, e, p, _ in w["sessions"] if p == pos)
                    rows.append((-t, wid, t))
            rows.sort(key=lambda r: (r[0], r[1]))
            results.append(", ".join("%s(%d)" % (wid, t) for _, wid, t in rows[:n]))
        elif name == "PROMOTE":
            wid, npos, ncomp, sts = op[1], op[2], int(op[3]), int(op[4])
            w = workers.get(wid)
            if w is None or w["pending"] is not None:
                results.append("invalid_request")
            else:
                w["pending"] = (npos, ncomp, sts)
                results.append("success")
        elif name == "SET_DOUBLE_PAID":
            grants.append((int(op[1]), int(op[2])))
            results.append("")
        elif name == "CALC_SALARY":
            wid, qs, qe = op[1], int(op[2]), int(op[3])
            w = workers.get(wid)
            if w is None:
                results.append("")
            else:
                starts, ends = merged()
                total = 0
                for s, e, _, comp in w["sessions"]:
                    lo = max(s, qs)
                    hi = min(e, qe)
                    if hi <= lo:
                        continue
                    rate = comp
                    if starts:
                        i = bisect.bisect_right(starts, s) - 1
                        if i >= 0 and ends[i] >= e:
                            rate = comp * 2
                    total += (hi - lo) * rate
                results.append(str(total))
        else:
            results.append("")
    return results

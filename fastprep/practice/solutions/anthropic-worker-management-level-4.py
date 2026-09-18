# Simulation: worker state machine with deferred promotions, session log, and a merged double-paid interval list.
from typing import List, Optional, Any
import bisect


def workerManagementLevel4(operations: List[List[str]]) -> List[str]:
    workers = {}
    out: List[str] = []
    dp_starts: List[int] = []
    dp_ends: List[int] = []

    def add_double_paid(s: int, e: int) -> None:
        if s >= e:
            return
        i = bisect.bisect_left(dp_ends, s)
        j = bisect.bisect_right(dp_starts, e)
        if i < j:
            s = min(s, dp_starts[i])
            e = max(e, dp_ends[j - 1])
            del dp_starts[i:j]
            del dp_ends[i:j]
        dp_starts.insert(i, s)
        dp_ends.insert(i, e)

    def double_paid_len(s: int, e: int) -> int:
        if s >= e:
            return 0
        total = 0
        i = bisect.bisect_right(dp_starts, s) - 1
        if i < 0:
            i = 0
        while i < len(dp_starts) and dp_starts[i] < e:
            lo = max(s, dp_starts[i])
            hi = min(e, dp_ends[i])
            if hi > lo:
                total += hi - lo
            i += 1
        return total

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
                    "entry_pos": None,
                    "entry_comp": None,
                    "total": 0,
                    "by_pos": {},
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
                    pending = w["pending"]
                    if pending is not None and ts >= pending[2]:
                        w["position"] = pending[0]
                        w["comp"] = pending[1]
                        w["pending"] = None
                    w["entry"] = ts
                    w["entry_pos"] = w["position"]
                    w["entry_comp"] = w["comp"]
                else:
                    start = w["entry"]
                    dur = ts - start
                    w["total"] += dur
                    w["by_pos"][w["entry_pos"]] = w["by_pos"].get(w["entry_pos"], 0) + dur
                    w["sessions"].append((start, ts, w["entry_comp"]))
                    w["entry"] = None
                    w["entry_pos"] = None
                    w["entry_comp"] = None
                out.append("registered")
        elif kind == "GET":
            w = workers.get(op[1])
            out.append("" if w is None else str(w["total"]))
        elif kind == "TOP_N_WORKERS":
            n, position = int(op[1]), op[2]
            cands = [
                (-w["by_pos"].get(position, 0), wid)
                for wid, w in workers.items()
                if w["position"] == position
            ]
            cands.sort()
            out.append(", ".join("%s(%d)" % (wid, -t) for t, wid in cands[:n]))
        elif kind == "PROMOTE":
            wid, position, comp, start = op[1], op[2], int(op[3]), int(op[4])
            w = workers.get(wid)
            if w is None or w["pending"] is not None:
                out.append("invalid_request")
            else:
                w["pending"] = (position, comp, start)
                out.append("success")
        elif kind == "CALC_SALARY":
            wid, lo, hi = op[1], int(op[2]), int(op[3])
            w = workers.get(wid)
            if w is None:
                out.append("")
            else:
                salary = 0
                for s, e, comp in w["sessions"]:
                    a, b = max(s, lo), min(e, hi)
                    if b > a:
                        salary += (b - a) * comp
                        salary += double_paid_len(a, b) * comp
                out.append(str(salary))
        elif kind == "SET_DOUBLE_PAID":
            add_double_paid(int(op[1]), int(op[2]))
            out.append("")
        else:
            out.append("")
    return out

# Event-ordered ledger simulation: rebate queue flushed by timestamp, per-workspace balance history via bisect.
from typing import List, Optional, Any
from bisect import bisect_right

REBATE_DELAY = 86400000


def processWorkspaceCreditOperations(operations: List[List[str]]) -> List[str]:
    ws = {}          # id -> dict(balance, activity, created, times[], bals[])
    txs = {}         # txid -> dict(owner, due, posted, amount)
    pending = []     # list of txids in creation order (dues nondecreasing)
    pend_i = 0
    tx_count = 0
    out = []

    def record(wid, t, bal):
        w = ws[wid]
        w["times"].append(t)
        w["bals"].append(bal)

    def flush(t):
        nonlocal pend_i
        while pend_i < len(pending):
            txid = pending[pend_i]
            tx = txs[txid]
            if tx["due"] > t:
                break
            pend_i += 1
            owner = tx["owner"]
            if owner in ws:
                ws[owner]["balance"] += tx["amount"]
                record(owner, tx["due"], ws[owner]["balance"])
            tx["posted"] = True

    for op in operations:
        kind = op[0]
        t = int(op[1])
        flush(t)
        if kind == "CREATE_WORKSPACE":
            wid = op[2]
            if wid in ws:
                out.append("false")
            else:
                ws[wid] = {"balance": 0, "activity": 0, "created": t,
                           "times": [t], "bals": [0]}
                out.append("true")
        elif kind == "ADD_CREDITS":
            wid = op[2]
            amount = int(op[3])
            if wid not in ws:
                out.append("")
            else:
                ws[wid]["balance"] += amount
                record(wid, t, ws[wid]["balance"])
                out.append(str(ws[wid]["balance"]))
        elif kind == "TRANSFER_CREDITS":
            src, dst = op[2], op[3]
            amount = int(op[4])
            if src not in ws or dst not in ws or src == dst or ws[src]["balance"] < amount:
                out.append("")
            else:
                ws[src]["balance"] -= amount
                ws[dst]["balance"] += amount
                ws[src]["activity"] += amount
                record(src, t, ws[src]["balance"])
                record(dst, t, ws[dst]["balance"])
                out.append(str(ws[src]["balance"]))
        elif kind == "TOP_WORKSPACES":
            n = int(op[2])
            items = sorted(ws.items(), key=lambda kv: (-kv[1]["activity"], kv[0]))[:n]
            out.append(",".join("%s(%d)" % (k, v["activity"]) for k, v in items))
        elif kind == "CONSUME_CREDITS":
            wid = op[2]
            amount = int(op[3])
            if wid not in ws or ws[wid]["balance"] < amount:
                out.append("")
            else:
                ws[wid]["balance"] -= amount
                ws[wid]["activity"] += amount
                record(wid, t, ws[wid]["balance"])
                tx_count += 1
                txid = "transaction%d" % tx_count
                txs[txid] = {"owner": wid, "due": t + REBATE_DELAY,
                             "posted": False, "amount": (amount * 2) // 100}
                pending.append(txid)
                out.append(txid)
        elif kind == "GET_REBATE_STATUS":
            txid = op[2]
            if txid not in txs:
                out.append("")
            else:
                out.append("RECEIVED" if txs[txid]["posted"] else "PENDING")
        elif kind == "MERGE_WORKSPACES":
            surv, absorbed = op[2], op[3]
            if surv not in ws or absorbed not in ws or surv == absorbed:
                out.append("false")
            else:
                ws[surv]["balance"] += ws[absorbed]["balance"]
                ws[surv]["activity"] += ws[absorbed]["activity"]
                for tx in txs.values():
                    if tx["owner"] == absorbed:
                        tx["owner"] = surv
                del ws[absorbed]
                record(surv, t, ws[surv]["balance"])
                out.append("true")
        elif kind == "GET_BALANCE":
            wid = op[2]
            time_at = int(op[3])
            if wid not in ws:
                out.append("")
            else:
                w = ws[wid]
                idx = bisect_right(w["times"], time_at) - 1
                if idx < 0:
                    out.append("")
                else:
                    out.append(str(w["bals"][idx]))
        else:
            out.append("")
    return out

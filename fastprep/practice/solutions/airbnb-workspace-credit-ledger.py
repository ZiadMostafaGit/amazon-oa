# Event-driven ledger simulation: a FIFO rebate queue drained before each op, plus per-workspace balance history with binary search.
from typing import List, Optional, Any
from bisect import bisect_right
from collections import deque

REBATE_DELAY = 86400000


def processWorkspaceCreditOperations(operations: List[List[str]]) -> List[str]:
    ws = {}          # id -> dict(balance, activity, active, times, bals)
    txs = {}         # txid -> dict(owner, due, amount, posted)
    queue = deque()  # txids in creation (== due) order
    tx_counter = 0
    out = []

    def record(wid, t):
        w = ws[wid]
        if w["times"] and w["times"][-1] == t:
            w["bals"][-1] = w["balance"]
        else:
            w["times"].append(t)
            w["bals"].append(w["balance"])

    def alive(wid):
        return wid in ws and ws[wid]["active"]

    def drain(t):
        while queue:
            tx = txs[queue[0]]
            if tx["due"] > t:
                break
            queue.popleft()
            tx["posted"] = True
            owner = tx["owner"]
            if alive(owner):
                ws[owner]["balance"] += tx["amount"]
                record(owner, tx["due"])

    for op in operations:
        kind = op[0]
        t = int(op[1])
        drain(t)

        if kind == "CREATE_WORKSPACE":
            wid = op[2]
            if alive(wid):
                out.append("false")
            else:
                ws[wid] = {"balance": 0, "activity": 0, "active": True,
                           "times": [t], "bals": [0]}
                out.append("true")

        elif kind == "ADD_CREDITS":
            wid, amount = op[2], int(op[3])
            if not alive(wid):
                out.append("")
            else:
                ws[wid]["balance"] += amount
                record(wid, t)
                out.append(str(ws[wid]["balance"]))

        elif kind == "TRANSFER_CREDITS":
            src, dst, amount = op[2], op[3], int(op[4])
            if src == dst or not alive(src) or not alive(dst) or ws[src]["balance"] < amount:
                out.append("")
            else:
                ws[src]["balance"] -= amount
                ws[dst]["balance"] += amount
                ws[src]["activity"] += amount
                record(src, t)
                record(dst, t)
                out.append(str(ws[src]["balance"]))

        elif kind == "TOP_WORKSPACES":
            n = int(op[2])
            live = [(wid, w["activity"]) for wid, w in ws.items() if w["active"]]
            live.sort(key=lambda p: (-p[1], p[0]))
            out.append(",".join("%s(%d)" % (wid, a) for wid, a in live[:n]))

        elif kind == "CONSUME_CREDITS":
            wid, amount = op[2], int(op[3])
            if not alive(wid) or ws[wid]["balance"] < amount:
                out.append("")
            else:
                ws[wid]["balance"] -= amount
                ws[wid]["activity"] += amount
                record(wid, t)
                tx_counter += 1
                txid = "transaction%d" % tx_counter
                txs[txid] = {"owner": wid, "due": t + REBATE_DELAY,
                             "amount": amount * 2 // 100, "posted": False}
                queue.append(txid)
                out.append(txid)

        elif kind == "GET_REBATE_STATUS":
            txid = op[2]
            if txid not in txs:
                out.append("")
            else:
                out.append("RECEIVED" if txs[txid]["posted"] else "PENDING")

        elif kind == "MERGE_WORKSPACES":
            surv, absorbed = op[2], op[3]
            if surv == absorbed or not alive(surv) or not alive(absorbed):
                out.append("false")
            else:
                ws[surv]["balance"] += ws[absorbed]["balance"]
                ws[surv]["activity"] += ws[absorbed]["activity"]
                ws[absorbed]["balance"] = 0
                ws[absorbed]["active"] = False
                for tx in txs.values():
                    if tx["owner"] == absorbed:
                        tx["owner"] = surv
                record(surv, t)
                out.append("true")

        elif kind == "GET_BALANCE":
            wid, time_at = op[2], int(op[3])
            if not alive(wid):
                out.append("")
            else:
                w = ws[wid]
                idx = bisect_right(w["times"], time_at)
                out.append("" if idx == 0 else str(w["bals"][idx - 1]))

        else:
            out.append("")

    return out

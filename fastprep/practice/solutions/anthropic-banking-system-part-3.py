from typing import List, Optional, Any
import heapq


def bankingSystemLevel3(operations: List[List[str]]) -> List[List[str]]:
    balances = {}
    outgoing = {}

    # pending payments: id -> dict(account, amount, exec_time, seq, active)
    payments = {}
    # min-heap of (exec_time, seq, payment_id)
    heap = []
    seq = 0
    next_payment = 1

    def run_due(t):
        while heap and heap[0][0] <= t:
            exec_time, _, pid = heapq.heappop(heap)
            info = payments.get(pid)
            if info is None or not info["active"]:
                continue
            info["active"] = False
            acct = info["account"]
            amt = info["amount"]
            if acct in balances and balances[acct] >= amt:
                balances[acct] -= amt
                outgoing[acct] = outgoing.get(acct, 0) + amt

    results = []
    for op in operations:
        name = op[0]
        ts = int(op[1])
        run_due(ts)

        if name == "CREATE_ACCOUNT":
            acct = op[2]
            if acct in balances:
                results.append(["false"])
            else:
                balances[acct] = 0
                outgoing[acct] = 0
                results.append(["true"])
        elif name == "DEPOSIT":
            acct = op[2]
            amount = int(op[3])
            if acct not in balances:
                results.append(["null"])
            else:
                balances[acct] += amount
                results.append([str(balances[acct])])
        elif name == "TRANSFER":
            src = op[2]
            dst = op[3]
            amount = int(op[4])
            if src not in balances or dst not in balances or src == dst or balances[src] < amount:
                results.append(["null"])
            else:
                balances[src] -= amount
                balances[dst] += amount
                outgoing[src] = outgoing.get(src, 0) + amount
                results.append([str(balances[src])])
        elif name == "TOP_SPENDERS":
            n = int(op[2])
            ranked = sorted(balances.keys(), key=lambda a: (-outgoing.get(a, 0), a))
            results.append(["%s(%d)" % (a, outgoing.get(a, 0)) for a in ranked[:n]])
        elif name == "SCHEDULE_PAYMENT":
            acct = op[2]
            amount = int(op[3])
            delay = int(op[4])
            if acct not in balances:
                results.append(["null"])
            else:
                pid = "payment%d" % next_payment
                next_payment += 1
                payments[pid] = {
                    "account": acct,
                    "amount": amount,
                    "active": True,
                }
                heapq.heappush(heap, (ts + delay, seq, pid))
                seq += 1
                results.append([pid])
        elif name == "CANCEL_PAYMENT":
            acct = op[2]
            pid = op[3]
            info = payments.get(pid)
            if info is None or not info["active"] or info["account"] != acct:
                results.append(["false"])
            else:
                info["active"] = False
                results.append(["true"])
        else:
            results.append(["null"])

    return results

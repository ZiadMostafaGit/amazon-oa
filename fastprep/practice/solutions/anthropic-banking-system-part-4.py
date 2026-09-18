from typing import List, Optional, Any
import heapq
from bisect import bisect_right


def bankingSystemLevel4(operations: List[List[str]]) -> List[List[str]]:
    balances = {}
    outgoing = {}

    # history[account] = (times, values); value None means "did not exist from here"
    hist_times = {}
    hist_vals = {}

    def record(acct, t, value):
        if acct not in hist_times:
            hist_times[acct] = []
            hist_vals[acct] = []
        hist_times[acct].append(t)
        hist_vals[acct].append(value)

    def lookup(acct, t):
        times = hist_times.get(acct)
        if not times:
            return None
        i = bisect_right(times, t)
        if i == 0:
            return None
        return hist_vals[acct][i - 1]

    payments = {}          # pid -> {"account", "amount", "active"}
    heap = []              # (exec_time, seq, pid)
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
                record(acct, exec_time, balances[acct])

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
                record(acct, ts, 0)
                results.append(["true"])
        elif name == "DEPOSIT":
            acct = op[2]
            amount = int(op[3])
            if acct not in balances:
                results.append(["null"])
            else:
                balances[acct] += amount
                record(acct, ts, balances[acct])
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
                record(src, ts, balances[src])
                record(dst, ts, balances[dst])
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
                payments[pid] = {"account": acct, "amount": amount, "active": True}
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
        elif name == "MERGE_ACCOUNTS":
            a1 = op[2]
            a2 = op[3]
            if a1 == a2 or a1 not in balances or a2 not in balances:
                results.append(["false"])
            else:
                balances[a1] += balances[a2]
                outgoing[a1] = outgoing.get(a1, 0) + outgoing.get(a2, 0)
                for info in payments.values():
                    if info["active"] and info["account"] == a2:
                        info["account"] = a1
                del balances[a2]
                outgoing.pop(a2, None)
                record(a1, ts, balances[a1])
                record(a2, ts, None)
                results.append(["true"])
        elif name == "GET_BALANCE":
            acct = op[2]
            time_at = int(op[3])
            value = lookup(acct, time_at)
            results.append(["null"] if value is None else [str(value)])
        else:
            results.append(["null"])

    return results

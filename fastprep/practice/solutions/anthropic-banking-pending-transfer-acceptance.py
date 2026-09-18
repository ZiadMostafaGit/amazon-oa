# Simulation: balances with reserved pending transfers, lazy expiry sweep before each operation.
from typing import List, Optional, Any


def bankingPendingTransferAcceptance(operations: List[List[str]]) -> List[List[str]]:
    balance = {}
    activity = {}
    pending = {}          # transfer_id -> dict(src, dst, amount, expires)
    order = []            # transfer ids in creation order (expiry order matches)
    counter = 0
    results = []

    def expire(now: int):
        i = 0
        for tid in order:
            info = pending.get(tid)
            if info is None:
                i += 1
                continue
            if info["expires"] < now:
                balance[info["src"]] += info["amount"]
                del pending[tid]
                i += 1
            else:
                break
        del order[:i]

    for op in operations:
        name = op[0]
        if name == "CREATE_ACCOUNT":
            ts = int(op[1])
            expire(ts)
            acc = op[2]
            if acc in balance:
                results.append(["false"])
            else:
                balance[acc] = 0
                activity[acc] = 0
                results.append(["true"])
        elif name == "DEPOSIT":
            ts = int(op[1])
            expire(ts)
            acc, amount = op[2], int(op[3])
            if acc not in balance:
                results.append(["null"])
            else:
                balance[acc] += amount
                activity[acc] += amount
                results.append([str(balance[acc])])
        elif name == "PAY":
            ts = int(op[1])
            expire(ts)
            acc, amount = op[2], int(op[3])
            if acc not in balance or balance[acc] < amount:
                results.append(["null"])
            else:
                balance[acc] -= amount
                activity[acc] += amount
                results.append([str(balance[acc])])
        elif name == "TRANSFER":
            ts = int(op[1])
            expire(ts)
            src, dst, amount = op[2], op[3], int(op[4])
            if src not in balance or dst not in balance or src == dst or balance[src] < amount:
                results.append(["null"])
            else:
                counter += 1
                tid = "transfer%d" % counter
                balance[src] -= amount
                pending[tid] = {"src": src, "dst": dst, "amount": amount,
                                "expires": ts + 86400000}
                order.append(tid)
                results.append([tid])
        elif name == "ACCEPT_TRANSFER":
            ts = int(op[1])
            expire(ts)
            acc, tid = op[2], op[3]
            info = pending.get(tid)
            if info is None or info["dst"] != acc:
                results.append(["false"])
            else:
                amount = info["amount"]
                balance[acc] += amount
                activity[acc] += amount
                activity[info["src"]] += amount
                del pending[tid]
                results.append(["true"])
        elif name == "TOP_ACTIVITY":
            ts = int(op[1])
            expire(ts)
            n = int(op[2])
            ranked = sorted(activity.items(), key=lambda kv: (-kv[1], kv[0]))
            results.append(["%s(%d)" % (a, v) for a, v in ranked[:max(n, 0)]])
        else:
            results.append([])
    return results

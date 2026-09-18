# Direct simulation with dicts for balance/activity and a sort for TOP_ACTIVITY ranking.
from typing import List, Optional, Any


def processBankingOperations(operations: List[List[str]]) -> List[List[str]]:
    balance = {}
    activity = {}
    out = []
    for op in operations:
        kind = op[0]
        if kind == "CREATE_ACCOUNT":
            acc = op[1]
            if acc in balance:
                out.append(["false"])
            else:
                balance[acc] = 0
                activity[acc] = 0
                out.append(["true"])
        elif kind == "DEPOSIT":
            acc = op[1]
            amt = int(op[2])
            if acc not in balance:
                out.append(["-1"])
            else:
                balance[acc] += amt
                activity[acc] += abs(amt)
                out.append([str(balance[acc])])
        elif kind == "TRANSFER":
            src, dst = op[1], op[2]
            amt = int(op[3])
            if src not in balance or dst not in balance or src == dst or balance[src] < amt:
                out.append(["-1"])
            else:
                balance[src] -= amt
                balance[dst] += amt
                activity[src] += abs(amt)
                activity[dst] += abs(amt)
                out.append([str(balance[src])])
        elif kind == "TOP_ACTIVITY":
            n = int(op[1])
            ranked = sorted(activity.items(), key=lambda kv: (-kv[1], kv[0]))
            out.append(["%s(%d)" % (a, v) for a, v in ranked[:max(n, 0)]])
        else:
            out.append([])
    return out

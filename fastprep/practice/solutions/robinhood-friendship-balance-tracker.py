# Direct state-machine simulation with hash maps for users, pending requests and friendships.
from typing import List, Optional, Any


def processFriendshipTransfers(operations: List[str]) -> List[str]:
    balances = {}
    pending = {}          # request id -> (from, to)
    friends = {}          # user -> set of friends
    out: List[str] = []

    for op in operations:
        parts = op.split()
        rid = parts[0]
        kind = parts[1]
        ok = False
        extra = ""

        if kind == "REGISTER":
            user = parts[2]
            amount = int(parts[3])
            if user not in balances and amount >= 0:
                balances[user] = amount
                friends[user] = set()
                ok = True
        elif kind == "REQUEST":
            src, dst = parts[2], parts[3]
            if src in balances and dst in balances and src != dst and dst not in friends[src]:
                pending[rid] = (src, dst)
                ok = True
        elif kind == "ACCEPT":
            target = parts[2]
            if target in pending:
                src, dst = pending.pop(target)
                friends[src].add(dst)
                friends[dst].add(src)
                ok = True
        elif kind == "TRANSFER":
            src, dst = parts[2], parts[3]
            amount = int(parts[4])
            if (src in balances and dst in balances and src != dst
                    and dst in friends[src] and amount >= 0 and balances[src] >= amount):
                balances[src] -= amount
                balances[dst] += amount
                ok = True
                extra = " %d %d" % (balances[src], balances[dst])

        out.append(rid + " OK" + extra if ok else rid + " REJECTED")

    return out

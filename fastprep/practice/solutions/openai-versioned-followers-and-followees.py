# Per-edge change history keyed by snapshot id; binary search the history to read a snapshot.
from typing import List, Optional, Any
from bisect import bisect_right


def getVersionedRelationships(n: int, operations: List[str]) -> List[str]:
    # edge (u, v) -> (list of snapshot ids, list of active flags), appended in order
    history = {}
    out_adj = {}  # u -> set of v ever followed
    in_adj = {}   # v -> set of u that ever followed
    snap = 0      # id that the next SNAPSHOT command will receive
    out = []

    def active_at(u, v, sid):
        h = history.get((u, v))
        if not h:
            return False
        keys, flags = h
        i = bisect_right(keys, sid)
        if i == 0:
            return False
        return flags[i - 1]

    for op in operations:
        parts = op.split()
        cmd = parts[0]
        if cmd == "FOLLOW" or cmd == "UNFOLLOW":
            u = int(parts[1])
            v = int(parts[2])
            state = cmd == "FOLLOW"
            h = history.get((u, v))
            if h is None:
                history[(u, v)] = ([snap], [state])
            else:
                h[0].append(snap)
                h[1].append(state)
            out_adj.setdefault(u, set()).add(v)
            in_adj.setdefault(v, set()).add(u)
        elif cmd == "SNAPSHOT":
            out.append(str(snap))
            snap += 1
        elif cmd == "GET_FOLLOWERS":
            user = int(parts[1])
            sid = int(parts[2])
            res = sorted(u for u in in_adj.get(user, ()) if active_at(u, user, sid))
            out.append("[" + ",".join(map(str, res)) + "]")
        elif cmd == "GET_FOLLOWEES":
            user = int(parts[1])
            sid = int(parts[2])
            res = sorted(v for v in out_adj.get(user, ()) if active_at(user, v, sid))
            out.append("[" + ",".join(map(str, res)) + "]")
    return out

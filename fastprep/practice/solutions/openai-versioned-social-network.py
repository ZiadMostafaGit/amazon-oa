from typing import List, Optional, Any
from bisect import bisect_right


def processVersionedSocialNetwork(n: int, operations: List[str]) -> List[str]:
    # For each directed edge we keep a change log: parallel lists of the
    # snapshot counter at the moment of the change and the resulting state.
    # A change made while `snap` snapshots exist is visible to snapshot ids
    # >= snap, so a query for snapshot q binary-searches the last entry with
    # recorded counter <= q.  O(log h) per query, O(c) total space.
    times = {}
    states = {}
    snap = 0
    out = []

    for op in operations:
        parts = op.split()
        cmd = parts[0]
        if cmd == "SNAPSHOT":
            out.append(str(snap))
            snap += 1
        elif cmd == "IS_FOLLOWING":
            u = int(parts[1])
            v = int(parts[2])
            q = int(parts[3])
            key = (u, v)
            ts = times.get(key)
            if not ts:
                out.append("false")
            else:
                i = bisect_right(ts, q) - 1
                if i < 0:
                    out.append("false")
                else:
                    out.append("true" if states[key][i] else "false")
        else:
            u = int(parts[1])
            v = int(parts[2])
            key = (u, v)
            active = (cmd == "FOLLOW")
            ts = times.get(key)
            if ts is None:
                times[key] = [snap]
                states[key] = [active]
            elif ts[-1] == snap:
                # Another change before any new snapshot: the snapshot only
                # records the state after the last such change.
                states[key][-1] = active
            else:
                ts.append(snap)
                states[key].append(active)

    return out

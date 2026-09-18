# Direct simulation of shared control blocks with strong/weak counters and per-operation state snapshots.
from typing import List, Optional, Any


def simulateReferenceControlBlocks(operations: List[List[str]]) -> List[str]:
    blocks = {}          # block id -> [strong, weak]
    handles = {}         # handle name -> (block id, kind)
    next_id = 0
    out = []

    def snapshot(bid):
        s, w = blocks[bid]
        state = "LIVE" if s > 0 else "EXPIRED"
        return "%d:%d:%s" % (s, w, state)

    for op in operations:
        kind = op[0]
        if kind == "CREATE":
            bid = next_id
            next_id += 1
            blocks[bid] = [1, 0]
            handles[op[1]] = (bid, "strong")
            out.append(snapshot(bid))
        elif kind == "CLONE_STRONG":
            bid = handles[op[1]][0]
            blocks[bid][0] += 1
            handles[op[2]] = (bid, "strong")
            out.append(snapshot(bid))
        elif kind == "MAKE_WEAK":
            bid = handles[op[1]][0]
            blocks[bid][1] += 1
            handles[op[2]] = (bid, "weak")
            out.append(snapshot(bid))
        elif kind == "LOCK_WEAK":
            bid = handles[op[1]][0]
            if blocks[bid][0] > 0:
                blocks[bid][0] += 1
                handles[op[2]] = (bid, "strong")
            out.append(snapshot(bid))
        elif kind == "RELEASE":
            bid, hkind = handles.pop(op[1])
            if hkind == "strong":
                blocks[bid][0] -= 1
            else:
                blocks[bid][1] -= 1
            if blocks[bid][0] == 0 and blocks[bid][1] == 0:
                del blocks[bid]
                out.append("0:0:REMOVED")
            else:
                out.append(snapshot(bid))
        else:  # QUERY
            bid = handles[op[1]][0]
            out.append(snapshot(bid))
    return out

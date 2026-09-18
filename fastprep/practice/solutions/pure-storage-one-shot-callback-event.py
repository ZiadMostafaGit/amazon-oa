# Linear simulation with a pending queue that is drained once on FIRE.
from typing import List, Optional, Any


def dispatchCallbacks(operations: List[List[str]]) -> List[List[str]]:
    pending = []
    fired = False
    out = []
    for op in operations:
        if op[0] == "FIRE":
            fired = True
            out.append(pending)
            pending = []
        else:
            cid = op[1]
            if fired:
                out.append([cid])
            else:
                pending.append(cid)
                out.append([])
    return out

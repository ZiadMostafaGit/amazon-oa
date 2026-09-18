# Hash map from token id to expiry time; counts scan live entries at each COUNT query.
from typing import List, Optional, Any


def countUnexpiredTokens(timeToLive: int, operations: List[List[str]]) -> List[int]:
    expiry = {}
    res = []
    for op in operations:
        kind, tid, t_s = op[0], op[1], op[2]
        t = int(t_s)
        if kind == "GENERATE":
            expiry[tid] = t + timeToLive
        elif kind == "RENEW":
            e = expiry.get(tid)
            if e is not None and e > t:
                expiry[tid] = t + timeToLive
        else:
            res.append(sum(1 for e in expiry.values() if e > t))
    return res

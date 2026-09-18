# Hash map from token id to expiry time; counts scan the map at each COUNT query.
from typing import List, Optional, Any


def countUnexpiredTokens(timeToLive: int, operations: List[List[str]]) -> List[int]:
    expiry = {}
    res = []
    for op in operations:
        kind = op[0]
        token = op[1]
        t = int(op[2])
        if kind == "GENERATE":
            expiry[token] = t + timeToLive
        elif kind == "RENEW":
            if token in expiry and expiry[token] > t:
                expiry[token] = t + timeToLive
        elif kind == "COUNT":
            # drop tokens already expired so the scan stays small
            dead = [k for k, e in expiry.items() if e <= t]
            for k in dead:
                del expiry[k]
            res.append(len(expiry))
    return res

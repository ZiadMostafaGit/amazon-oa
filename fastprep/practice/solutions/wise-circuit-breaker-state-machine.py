# Direct finite-state-machine simulation of CLOSED / OPEN / HALF_OPEN probe transitions.
from typing import List, Optional, Any


def runCircuitBreaker(requests: List[List[str]], failureThreshold: int, openDuration: int) -> List[str]:
    out = []
    state_open = False
    reopen_at = 0
    fails = 0
    for row in requests:
        ts = int(row[0])
        ok = row[1] == "SUCCESS"
        if state_open:
            if ts < reopen_at:
                out.append("REJECTED:OPEN")
                continue
            # half-open probe
            if ok:
                state_open = False
                fails = 0
                out.append("ALLOWED:CLOSED")
            else:
                reopen_at = ts + openDuration
                out.append("ALLOWED:OPEN")
            continue
        if ok:
            fails = 0
            out.append("ALLOWED:CLOSED")
        else:
            fails += 1
            if fails >= failureThreshold:
                state_open = True
                reopen_at = ts + openDuration
                fails = 0
                out.append("ALLOWED:OPEN")
            else:
                out.append("ALLOWED:CLOSED")
    return out

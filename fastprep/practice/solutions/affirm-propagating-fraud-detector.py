# Single pass with a suspicious set of (field index, value) pairs that grows on each tainted event.
from typing import List, Optional, Any


def detectPropagatingFraud(events: List[List[str]]) -> List[str]:
    suspicious = set()
    out = []
    for row in events:
        entries = [(i, row[i]) for i in range(1, min(5, len(row))) if row[i]]
        if row and row[0] == "fraud_flag":
            suspicious.update(entries)
            out.append("")
        else:
            tainted = any(e in suspicious for e in entries)
            if tainted:
                suspicious.update(entries)
                out.append("1")
            else:
                out.append("0")
    return out

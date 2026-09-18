# Per-key append-only timestamp list; each get is a binary search for the greatest timestamp <= query.
import bisect
from typing import List, Optional, Any


def runTimeMap(operations: List[str], keys: List[str], values: List[str], timestamps: List[int]) -> List[str]:
    store: dict = {}
    output: List[str] = []
    for op, key, value, stamp in zip(operations, keys, values, timestamps):
        if op == "set":
            times, vals = store.setdefault(key, ([], []))
            position = bisect.bisect_right(times, stamp)
            times.insert(position, stamp)
            vals.insert(position, value)
            output.append("null")
        else:
            if key not in store:
                output.append("")
                continue
            times, vals = store[key]
            position = bisect.bisect_right(times, stamp)
            output.append(vals[position - 1] if position else "")
    return output

# Hash map from key to its best (timestamp, value); a write wins on a timestamp >= the stored one.
from typing import List, Optional, Any


def latestTimestampValues(operations: List[int], keys: List[str], values: List[str], timestamps: List[int]) -> List[str]:
    store = {}
    out: List[str] = []
    for i in range(len(operations)):
        key = keys[i]
        if operations[i] == 0:
            current = store.get(key)
            if current is None or timestamps[i] >= current[0]:
                store[key] = (timestamps[i], values[i])
        else:
            current = store.get(key)
            out.append(current[1] if current is not None else "")
    return out

# Per-key append-only version history plus binary search (bisect) for historical reads.
from typing import List, Optional, Any
from bisect import bisect_right


def runVersionedStore(operations: List[str]) -> List[str]:
    versions = {}   # key -> list of global versions (increasing)
    values = {}     # key -> list of values, parallel to versions
    out = []
    global_version = 0
    for op in operations:
        parts = op.split(' ')
        cmd = parts[0]
        if cmd == 'SET':
            key, value = parts[1], parts[2]
            global_version += 1
            if key not in versions:
                versions[key] = []
                values[key] = []
            versions[key].append(global_version)
            values[key].append(value)
        elif cmd == 'GET':
            key = parts[1]
            if key in values and values[key]:
                out.append(values[key][-1])
            else:
                out.append("NULL")
        else:  # GET_AT
            key = parts[1]
            target = int(parts[2])
            if key in versions:
                idx = bisect_right(versions[key], target)
                out.append(values[key][idx - 1] if idx > 0 else "NULL")
            else:
                out.append("NULL")
    return out

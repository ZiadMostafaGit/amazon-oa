# Per-key sorted version list with binary search: floor lookup for GET, suffix truncation for DELETE.
from bisect import bisect_left, bisect_right, insort
from typing import List, Optional, Any


def processVersionedStore(operations: List[List[str]]) -> List[str]:
    versions = {}   # key -> sorted list of versions
    values = {}     # key -> {version: value}
    out = []

    for op in operations:
        kind = op[0]
        if kind == "PUT":
            key = op[1]
            ver = int(op[2])
            val = op[3]
            vs = versions.get(key)
            if vs is None:
                vs = []
                versions[key] = vs
                values[key] = {}
            i = bisect_left(vs, ver)
            if i == len(vs) or vs[i] != ver:
                vs.insert(i, ver)
            values[key][ver] = val
            out.append("null")
        elif kind == "GET":
            key = op[1]
            ver = int(op[2])
            vs = versions.get(key)
            if not vs:
                out.append("null")
            else:
                i = bisect_right(vs, ver)
                if i == 0:
                    out.append("null")
                else:
                    out.append(values[key][vs[i - 1]])
        else:  # DELETE
            key = op[1]
            ver = int(op[2])
            vs = versions.get(key)
            if vs:
                i = bisect_left(vs, ver)
                store = values[key]
                for v in vs[i:]:
                    store.pop(v, None)
                del vs[i:]
            out.append("null")
    return out

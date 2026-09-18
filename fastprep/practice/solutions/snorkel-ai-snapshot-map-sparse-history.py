# Per-key sparse version lists keyed by snapshot id, with binary search for historical reads.
from typing import List, Optional, Any
from bisect import bisect_right

NULL = "<NULL>"


def runSnapshotMap(operations: List[List[str]]) -> List[str]:
    vers = {}   # key -> list of snapshot ids
    vals = {}   # key -> list of values (None means deleted)
    counter = 0
    out = []

    def mutate(key, newval):
        vs = vers.get(key)
        if not vs:
            if newval is None:
                return
            vers[key] = [counter]
            vals[key] = [newval]
            return
        va = vals[key]
        if va[-1] == newval:
            return
        if vs[-1] == counter:
            prev = va[-2] if len(va) >= 2 else None
            if prev == newval:
                vs.pop()
                va.pop()
            else:
                va[-1] = newval
        else:
            vs.append(counter)
            va.append(newval)

    for op in operations:
        kind = op[0]
        if kind == "PUT":
            mutate(op[1], op[2])
        elif kind == "DELETE":
            mutate(op[1], None)
        elif kind == "GET":
            va = vals.get(op[1])
            v = va[-1] if va else None
            out.append(v if v is not None else NULL)
        elif kind == "SNAPSHOT":
            out.append(str(counter))
            counter += 1
        else:  # GET_AT
            key = op[1]
            sid = int(op[2])
            vs = vers.get(key)
            if not vs:
                out.append(NULL)
            else:
                i = bisect_right(vs, sid) - 1
                if i < 0:
                    out.append(NULL)
                else:
                    v = vals[key][i]
                    out.append(v if v is not None else NULL)
    return out

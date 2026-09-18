# Validate names against a field->index map, then scan records applying filters and projecting selected columns.
from typing import List


def projectAndFilterRecords(fieldNames: List[str], records: List[List[str]], selectedFields: List[str], filters: List[List[str]]) -> List[List[str]]:
    index = {name: i for i, name in enumerate(fieldNames)}
    for name in selectedFields:
        if name not in index:
            return [["INVALID"]]
    for f in filters:
        if f[0] not in index:
            return [["INVALID"]]
    conds = [(index[f[0]], f[1]) for f in filters]
    cols = [index[name] for name in selectedFields]
    out = []
    for rec in records:
        ok = True
        for col, expected in conds:
            if rec[col] != expected:
                ok = False
                break
        if ok:
            out.append([rec[c] for c in cols])
    return out

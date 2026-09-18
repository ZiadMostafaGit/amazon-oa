# Dict of key -> dict of field -> (value, expiry), with liveness checked lazily at each operation's timestamp.
from typing import List, Optional, Any


def processTemporalDatabase(operations: List[List[str]]) -> List[List[str]]:
    db = {}
    results = []
    for op in operations:
        kind = op[0]
        ts = int(op[1])
        key = op[2]
        if kind == "SET":
            db.setdefault(key, {})[op[3]] = (op[4], None)
            results.append(["true"])
        elif kind == "SET_WITH_TTL":
            db.setdefault(key, {})[op[3]] = (op[4], ts + int(op[5]))
            results.append(["true"])
        elif kind == "DELETE":
            field = op[3]
            record = db.get(key)
            removed = False
            if record is not None and field in record:
                value, expiry = record[field]
                if expiry is None or expiry > ts:
                    removed = True
                del record[field]
            results.append(["true"] if removed else ["false"])
        else:
            prefix = op[3] if kind == "SCAN_BY_PREFIX" else ""
            record = db.get(key, {})
            out = []
            for field in record:
                if prefix and not field.startswith(prefix):
                    continue
                value, expiry = record[field]
                if expiry is None or expiry > ts:
                    out.append(field + "(" + value + ")")
            out.sort()
            results.append(out)
    return results

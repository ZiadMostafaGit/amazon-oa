# Simulation: dict-of-dicts store with per-field expiry timestamps plus timestamped backups.
from typing import List, Optional, Any


def runInMemoryDatabase(operations: List[List[str]]) -> List[List[str]]:
    # key -> field -> (value, expire_at or None)
    db = {}
    backups = []  # list of (timestamp, snapshot) sorted by timestamp

    def alive(entry, ts):
        exp = entry[1]
        return exp is None or ts < exp

    def rec(key, ts):
        r = db.get(key)
        if not r:
            return {}
            
        return {f: e for f, e in r.items() if alive(e, ts)}

    def do_set(key, field, value, ts, ttl=None):
        r = db.setdefault(key, {})
        # drop expired entries lazily
        for f in [f for f, e in r.items() if not alive(e, ts)]:
            del r[f]
        r[field] = (value, None if ttl is None else ts + ttl)

    def do_get(key, field, ts):
        r = db.get(key)
        if not r:
            return None
        e = r.get(field)
        if e is None or not alive(e, ts):
            return None
        return e[0]

    def do_delete(key, field, ts):
        r = db.get(key)
        if not r:
            return False
        e = r.get(field)
        if e is None or not alive(e, ts):
            if e is not None:
                del r[field]
            return False
        del r[field]
        return True

    def do_scan(key, ts, prefix=""):
        r = rec(key, ts)
        fields = sorted(f for f in r if f.startswith(prefix))
        return ["{}({})".format(f, r[f][0]) for f in fields]

    results = []
    for op in operations:
        name = op[0]
        if name == "set":
            do_set(op[1], op[2], op[3], 0)
            results.append([])
        elif name == "setAt":
            do_set(op[1], op[2], op[3], int(op[4]))
            results.append([])
        elif name == "setAtWithTtl":
            do_set(op[1], op[2], op[3], int(op[4]), int(op[5]))
            results.append([])
        elif name == "get":
            v = do_get(op[1], op[2], 0)
            results.append([] if v is None else [v])
        elif name == "getAt":
            v = do_get(op[1], op[2], int(op[3]))
            results.append([] if v is None else [v])
        elif name == "delete":
            results.append(["true"] if do_delete(op[1], op[2], 0) else ["false"])
        elif name == "deleteAt":
            results.append(["true"] if do_delete(op[1], op[2], int(op[3])) else ["false"])
        elif name == "scan":
            results.append(do_scan(op[1], 0))
        elif name == "scanAt":
            results.append(do_scan(op[1], int(op[2])))
        elif name == "scanByPrefix":
            results.append(do_scan(op[1], 0, op[2]))
        elif name == "scanByPrefixAt":
            results.append(do_scan(op[1], int(op[3]), op[2]))
        elif name == "backup":
            ts = int(op[1])
            snap = {}
            count = 0
            for key in db:
                live = rec(key, ts)
                if not live:
                    continue
                count += 1
                snap[key] = {
                    f: (e[0], None if e[1] is None else e[1] - ts)
                    for f, e in live.items()
                }
            backups.append((ts, snap))
            results.append([str(count)])
        elif name == "restore":
            ts = int(op[1])
            target = int(op[2])
            chosen = None
            for bts, snap in backups:
                if bts <= target:
                    chosen = snap
                else:
                    break
            db = {}
            if chosen is not None:
                for key, fields in chosen.items():
                    db[key] = {
                        f: (v, None if rem is None else ts + rem)
                        for f, (v, rem) in fields.items()
                    }
            results.append([])
        else:
            results.append([])
    return results

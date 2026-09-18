# Simulation: store records in insertion order, filter by name + tag subset, sort by (timestamp, insertion index) descending.
from typing import List, Optional, Any


def processMetrics(operations: List[List[str]]) -> List[List[str]]:
    store = []  # (name, ts_int, ts_str, value_str, tags_dict, index)
    result: List[List[str]] = []
    for op in operations:
        kind = op[0]
        if kind == "RECORD":
            name = op[1]
            ts_str = op[2]
            value_str = op[3]
            tags = {}
            for t in op[4:]:
                k, _, v = t.partition("=")
                tags[k] = v
            store.append((name, int(ts_str), ts_str, value_str, tags, len(store)))
            result.append(["null"])
        else:
            name = op[1]
            n = int(op[2])
            query = {}
            for t in op[3:]:
                k, _, v = t.partition("=")
                query[k] = v
            matches = []
            for rec in store:
                if rec[0] != name:
                    continue
                tags = rec[4]
                ok = True
                for k, v in query.items():
                    if tags.get(k) != v:
                        ok = False
                        break
                if ok:
                    matches.append(rec)
            matches.sort(key=lambda r: (-r[1], -r[5]))
            row = []
            for rec in matches[:n] if n > 0 else []:
                tag_str = ",".join(k + "=" + rec[4][k] for k in sorted(rec[4]))
                row.append("%s|%s|%s|%s" % (rec[0], rec[2], rec[3], tag_str))
            result.append(row)
    return result

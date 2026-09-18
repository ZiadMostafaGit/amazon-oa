from typing import List

WEEK = 10080


def _union(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def _subtract(keep, drop):
    drop = _union(drop)
    res = []
    for s, e in keep:
        cur = s
        for bs, be in drop:
            if be <= cur or bs >= e:
                continue
            if bs > cur:
                res.append([cur, min(bs, e)])
            cur = max(cur, be)
            if cur >= e:
                break
        if cur < e:
            res.append([cur, e])
    return res


def _to_utc(start, end, offset):
    """local minute-of-week -> UTC, split at the weekly boundary."""
    length = end - start
    if length <= 0:
        return []
    s = (start - offset) % WEEK
    if s + length <= WEEK:
        return [[s, s + length]]
    return [[s, WEEK], [0, min(s + length - WEEK, WEEK)]]


def scheduleDeploymentWindows(part: str, inputCsv: List[str]) -> List[List[int]]:
    allowed, freeze = [], []
    if part == "part1":
        for row in inputCsv:
            f = [x.strip() for x in row.split(",")]
            s, e, kind = int(f[0]), int(f[1]), f[2]
            (allowed if kind == "allowed" else freeze).append([s, e])
        return [list(x) for x in _union(_subtract(_union(allowed), freeze))]

    head = [int(x) for x in inputCsv[0].split(",")]
    utc_now, lead, min_len, k = head[0], head[1], head[2], head[3]
    for row in inputCsv[1:]:
        f = [x.strip() for x in row.split(",")]
        s, e, kind = int(f[0]), int(f[1]), f[2]
        off = int(f[3]) if len(f) > 3 else 0
        (allowed if kind == "allowed" else freeze).extend(_to_utc(s, e, off))

    windows = _union(_subtract(_union(allowed), freeze))
    earliest = utc_now + lead
    out = []
    for s, e in windows:
        s = max(s, earliest)
        e = min(e, WEEK)
        if e - s >= min_len and e - s > 0:
            out.append([s, e])
    out.sort()
    return out[:k]

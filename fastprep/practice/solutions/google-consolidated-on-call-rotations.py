from typing import List, Optional, Any
from collections import defaultdict


def getOnCallSchedule(rotations: List[str]) -> List[str]:
    events = defaultdict(list)  # time -> list of (name, +1/-1)
    for r in rotations:
        name, s, e = r.rsplit(",", 2)
        s, e = int(s), int(e)
        if s < e:
            events[s].append((name, 1))
            events[e].append((name, -1))
    count = defaultdict(int)
    active = set()
    segs = []  # [start, end, sorted names]
    prev_t = None
    for t in sorted(events):
        if prev_t is not None and active:
            if segs and segs[-1][1] == prev_t and not changed:
                segs[-1][1] = t
            else:
                segs.append([prev_t, t, sorted(active)])
        touched = set()
        for name, d in events[t]:
            count[name] += d
            touched.add(name)
        changed = False
        for name in touched:
            now = count[name] > 0
            if now != (name in active):
                changed = True
                if now:
                    active.add(name)
                else:
                    active.discard(name)
        prev_t = t
    return ["%d,%d,%s" % (s, e, ",".join(names)) for s, e, names in segs]

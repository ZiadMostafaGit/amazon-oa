# Validate/dedupe records, merge 10-minute slots per (provider,type), slide 30-minute windows, then bisect-match LAB->CONSULTATION within a 60-minute wait.
from typing import List, Optional, Any
from bisect import bisect_left, bisect_right

_VALID_TYPES = ("LAB", "CONSULTATION")


def _parse_time(s: str) -> Optional[int]:
    # exact 24-hour HH:MM form
    if len(s) != 5 or s[2] != ":":
        return None
    hh, mm = s[:2], s[3:]
    if not (hh.isdigit() and mm.isdigit()):
        return None
    h, m = int(hh), int(mm)
    if h > 23 or m > 59:
        return None
    return h * 60 + m


def _fmt(t: int) -> str:
    return "%02d:%02d" % (t // 60, t % 60)


def findAppointmentCombinations(providers: List[str], appointmentTypes: List[str], startTimes: List[str], endTimes: List[str]) -> List[List[str]]:
    n = min(len(providers), len(appointmentTypes), len(startTimes), len(endTimes))

    # group[(provider, type)] = set of valid 10-minute slot start times
    groups = {}
    for i in range(n):
        p = providers[i]
        t = appointmentTypes[i]
        if not p or t not in _VALID_TYPES:
            continue
        st = _parse_time(startTimes[i])
        if st is None:
            continue
        en = _parse_time(endTimes[i])
        if en is None or en - st != 10:
            continue
        key = (p, t)
        bucket = groups.get(key)
        if bucket is None:
            bucket = set()
            groups[key] = bucket
        bucket.add(st)

    labs = []   # (start_minute, provider)
    cons = []   # (start_minute, provider)
    for (provider, typ), slots in groups.items():
        target = labs if typ == "LAB" else cons
        ordered = sorted(slots)
        i = 0
        L = len(ordered)
        while i < L:
            j = i
            while j + 1 < L and ordered[j + 1] - ordered[j] == 10:
                j += 1
            # merged interval covers slots ordered[i..j]; 30-min window needs 3 slots
            for k in range(i, j - 1):
                target.append((ordered[k], provider))
            i = j + 1

    labs.sort()
    cons.sort()
    cons_starts = [c[0] for c in cons]

    out = []
    for lab_start, lab_provider in labs:
        lab_end = lab_start + 30
        lo = bisect_left(cons_starts, lab_end)
        hi = bisect_right(cons_starts, lab_end + 60)
        if lo >= hi:
            continue
        lab_s, lab_e = _fmt(lab_start), _fmt(lab_end)
        for idx in range(lo, hi):
            cs, cp = cons[idx]
            out.append([lab_provider, lab_s, lab_e, cp, _fmt(cs), _fmt(cs + 30)])

    out.sort(key=lambda r: (r[1], r[0], r[4], r[3]))
    return out

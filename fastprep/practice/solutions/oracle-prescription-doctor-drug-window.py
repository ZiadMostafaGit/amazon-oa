# Per (patient, drug) sliding window over dates, keeping a doctor multiset for
# the trailing 30 days; a second distinct doctor in the window emits the pair.
from typing import List, Optional, Any
from collections import deque, Counter
from datetime import date


def _to_ordinal(s: str) -> int:
    y, m, d = s.split("-")
    return date(int(y), int(m), int(d)).toordinal()


def findCrossDoctorPrescriptions(records: List[List[str]]) -> List[str]:
    windows = {}          # key -> deque of (ordinal, doctor)
    doctors = {}          # key -> Counter of doctor -> count inside window
    done = set()
    out = []

    for rec in records:
        patient, doctor, drug, day = rec[0], rec[1], rec[2], rec[3]
        key = (patient, drug)
        if key in done:
            continue
        cur = _to_ordinal(day)

        dq = windows.get(key)
        if dq is None:
            dq = deque()
            windows[key] = dq
            doctors[key] = Counter()
        cnt = doctors[key]

        while dq and cur - dq[0][0] > 30:
            old_day, old_doc = dq.popleft()
            cnt[old_doc] -= 1
            if cnt[old_doc] == 0:
                del cnt[old_doc]

        # a different doctor still inside the 30-day window means the pair qualifies
        qualifies = bool(cnt) and (len(cnt) > 1 or doctor not in cnt)

        dq.append((cur, doctor))
        cnt[doctor] += 1

        if qualifies:
            done.add(key)
            windows.pop(key, None)
            doctors.pop(key, None)
            out.append(patient + " " + drug)

    return out

# Streaming sliding window (two pointers) over the logs with per-merchant/per-code counters.
from typing import Dict, List


def detectIncidents(logs: List[str]) -> List[str]:
    parsed = []
    for line in logs:
        ts, merchant, code, count = line.split(",")
        parsed.append((int(ts), merchant, code, int(count)))

    # merchant -> code -> total count currently inside the window
    window: Dict[str, Dict[str, int]] = {}
    active = set()  # (merchant, code) pairs with an open alert
    events = []
    left = 0

    def add(entry, sign):
        _, merchant, code, count = entry
        codes = window.setdefault(merchant, {})
        new = codes.get(code, 0) + sign * count
        if new == 0:
            codes.pop(code, None)
            if not codes:
                window.pop(merchant, None)
        else:
            codes[code] = new

    for i, entry in enumerate(parsed):
        ts, merchant, code, _ = entry
        add(entry, 1)
        start = ts - 29
        while parsed[left][0] < start:
            add(parsed[left], -1)
            left += 1

        codes = window.get(merchant, {})
        success = codes.get("200", 0)
        to_check = set(c for c in codes if c != "200")
        to_check.update(c for (m, c) in active if m == merchant)
        if code != "200":
            to_check.add(code)

        for c in sorted(to_check):
            failures = codes.get(c, 0)
            fires = failures >= 5 and failures * 100 > success
            key = (merchant, c)
            if fires:
                if key not in active:
                    active.add(key)
                    events.append((ts, merchant, c, "TRIGGER"))
            elif key in active:
                active.discard(key)
                events.append((ts, merchant, c, "RESOLVE"))

    events.sort()
    return ["%d,%s,%s,%s" % (ts, kind, merchant, code) for ts, merchant, code, kind in events]

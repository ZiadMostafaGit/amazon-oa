# Approach: per-minute simulation in integer cents with store-wait override and peak-window doubling.
from typing import List, Optional, Any


def _t(s: str) -> int:
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def calculateDasherPay(events: List[str], peakHours: List[str]) -> float:
    parsed = []
    for e in events:
        p = e.split()
        parsed.append((_t(p[0]), p[1], p[2] if len(p) > 2 else ""))

    peak = [False] * (24 * 60 + 1)
    for w in peakHours:
        p = w.split()
        s, e = _t(p[0]), _t(p[1])
        for m in range(s, min(e, 24 * 60)):
            peak[m] = True

    active = set()
    waiting = None
    cents = 0
    for i, (t, kind, oid) in enumerate(parsed):
        if kind == "ACCEPT":
            active.add(oid)
        elif kind == "ARRIVE":
            waiting = oid
        elif kind == "PICKUP":
            waiting = None
        else:
            active.discard(oid)
        if i + 1 < len(parsed):
            nxt = parsed[i + 1][0]
            rate = 30 * (1 if (waiting is not None and waiting in active) else len(active))
            for m in range(t, nxt):
                cents += rate * (2 if peak[m] else 1)
    return cents / 100.0

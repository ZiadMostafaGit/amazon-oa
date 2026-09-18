# Hash map of key -> (value, expiry) plus a lazy min-heap of expiries and running sum/count.
import heapq
from fractions import Fraction
from typing import List


def processWindowedMap(operations: List[str], windowSeconds: int) -> List[str]:
    active = {}                # key -> (value, expiry)
    pending = []               # min-heap of (expiry, key)
    total = 0
    count = 0
    out = []

    def expire(now: int) -> None:
        nonlocal total, count
        while pending and pending[0][0] <= now:
            exp, key = heapq.heappop(pending)
            entry = active.get(key)
            if entry is not None and entry[1] == exp:
                del active[key]
                total -= entry[0]
                count -= 1

    def drop(key: str) -> None:
        nonlocal total, count
        entry = active.pop(key, None)
        if entry is not None:
            total -= entry[0]
            count -= 1

    for line in operations:
        parts = line.split()
        cmd = parts[0]
        now = int(parts[1])
        expire(now)
        if cmd == "put":
            key = parts[2]
            value = int(parts[3])
            drop(key)
            expiry = now + windowSeconds
            active[key] = (value, expiry)
            total += value
            count += 1
            heapq.heappush(pending, (expiry, key))
        elif cmd == "get":
            entry = active.get(parts[2])
            out.append("NOT_FOUND" if entry is None else str(entry[0]))
        elif cmd == "delete":
            drop(parts[2])
        elif cmd == "average":
            if count == 0:
                out.append("EMPTY")
            else:
                frac = Fraction(total, count)
                if frac.denominator == 1:
                    out.append(str(frac.numerator))
                else:
                    out.append(f"{frac.numerator}/{frac.denominator}")
    return out

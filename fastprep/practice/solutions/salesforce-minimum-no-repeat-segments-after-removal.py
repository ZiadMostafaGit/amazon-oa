# Try each of the 26 removable letters; greedy left-to-right partition gives the minimum segments.


def getNoRepeatSegments(s: str) -> int:
    present = set(s)
    best = None
    for c in "abcdefghijklmnopqrstuvwxyz":
        if c not in present:
            continue
        segments = 0
        seen = 0  # bitmask of letters in the current segment
        empty = True
        for ch in s:
            if ch == c:
                continue
            empty = False
            bit = 1 << (ord(ch) - 97)
            if seen & bit:
                segments += 1
                seen = bit
            else:
                seen |= bit
        if not empty:
            segments += 1
        if best is None or segments < best:
            best = segments
    return 0 if best is None else best

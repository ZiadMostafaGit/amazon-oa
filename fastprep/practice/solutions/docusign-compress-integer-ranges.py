# Sort distinct values, then emit maximal consecutive runs.
from typing import List


def compressRanges(nums: List[int]) -> str:
    vals = sorted(set(nums))
    if not vals:
        return ""
    parts = []
    start = vals[0]
    prev = vals[0]
    for v in vals[1:]:
        if v == prev + 1:
            prev = v
            continue
        parts.append(str(start) if start == prev else "%d-%d" % (start, prev))
        start = prev = v
    parts.append(str(start) if start == prev else "%d-%d" % (start, prev))
    return ",".join(parts)

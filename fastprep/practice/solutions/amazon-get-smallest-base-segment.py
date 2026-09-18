# Binary search the minimum replication count k, then greedily pad leftover slots with 'a'.
from collections import Counter


def getSmallestBaseSegment(segmentSize: int, missingData: str) -> str:
    need = Counter(missingData)
    if len(need) > segmentSize:
        return "-1"

    def slots(k: int) -> int:
        return sum((c + k - 1) // k for c in need.values())

    lo, hi = 1, max(need.values())
    while lo < hi:
        mid = (lo + hi) // 2
        if slots(mid) <= segmentSize:
            hi = mid
        else:
            lo = mid + 1
    k = lo

    counts = {ch: (c + k - 1) // k for ch, c in need.items()}
    leftover = segmentSize - sum(counts.values())
    if leftover > 0:
        counts['a'] = counts.get('a', 0) + leftover
    return ''.join(ch * counts[ch] for ch in sorted(counts))

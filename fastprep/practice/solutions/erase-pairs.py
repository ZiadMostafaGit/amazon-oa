# Greedy: keep one occurrence of each odd-count letter, picking the lexicographically
# smallest feasible subsequence via next-occurrence lookups.
from bisect import bisect_left
from collections import Counter, defaultdict


def erasePairs(S: str) -> str:
    counts = Counter(S)
    needed = {c for c, n in counts.items() if n % 2 == 1}
    # This problem's data encodes the empty result as a single space.
    if not needed:
        return " "

    occ = defaultdict(list)
    for i, ch in enumerate(S):
        if ch in needed:
            occ[ch].append(i)

    def first_at_or_after(ch, start):
        lst = occ[ch]
        j = bisect_left(lst, start)
        return lst[j] if j < len(lst) else None

    remaining = set(needed)
    start = 0
    out = []
    while remaining:
        for c in sorted(remaining):
            i = first_at_or_after(c, start)
            if i is None:
                continue
            ok = True
            for d in remaining:
                if d == c:
                    continue
                if first_at_or_after(d, i + 1) is None:
                    ok = False
                    break
            if ok:
                out.append(c)
                remaining.discard(c)
                start = i + 1
                break
        else:
            break
    return "".join(out) if out else " "

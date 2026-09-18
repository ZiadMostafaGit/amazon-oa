# Group visits per user, stable-sort by timestamp, count distinct users per consecutive triple.
from typing import List, Optional, Any
from collections import defaultdict


def mostFrequentConsecutivePattern(usernames: List[str], timestamps: List[int], websites: List[str]) -> List[str]:
    per_user = defaultdict(list)
    for i, u in enumerate(usernames):
        per_user[u].append(i)

    counts = defaultdict(int)
    for u, idxs in per_user.items():
        idxs.sort(key=lambda i: (timestamps[i], i))
        sites = [websites[i] for i in idxs]
        seen = set()
        for j in range(len(sites) - 2):
            seen.add((sites[j], sites[j + 1], sites[j + 2]))
        for pat in seen:
            counts[pat] += 1

    if not counts:
        return []
    # pick max count, tie-break lexicographically smallest
    best_pat = None
    best_cnt = -1
    for pat, c in counts.items():
        if c > best_cnt or (c == best_cnt and list(pat) < list(best_pat)):
            best_cnt = c
            best_pat = pat
    return list(best_pat)

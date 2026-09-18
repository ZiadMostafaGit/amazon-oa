# Sort requirements + prefix sums, then for each container set binary-search the bucket each size covers.
from bisect import bisect_right
from typing import List


def chooseContainers(requirements: List[int], numContainerSets: int, containers: List[List[int]]) -> int:
    reqs = sorted(requirements)
    n = len(reqs)
    prefix = [0] * (n + 1)
    for i, v in enumerate(reqs):
        prefix[i + 1] = prefix[i] + v

    groups = {}
    for row in containers:
        sid, size = row[0], row[1]
        groups.setdefault(sid, []).append(size)

    best_idx = -1
    best_waste = None
    for sid in sorted(groups):
        sizes = sorted(groups[sid])
        prev = 0
        waste = 0
        for s in sizes:
            idx = bisect_right(reqs, s)
            if idx > prev:
                waste += s * (idx - prev) - (prefix[idx] - prefix[prev])
                prev = idx
        if prev < n:
            continue  # some requirement exceeds the largest container in this set
        if best_waste is None or waste < best_waste:
            best_waste = waste
            best_idx = sid
    return best_idx

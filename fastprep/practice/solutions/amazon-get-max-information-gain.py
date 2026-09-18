# Sort by length, then for each pair (checked from the widest gap inward) test
# common features as sum of min character counts; 26-letter counts make each check O(26).
from typing import List, Optional, Any


def getMaxInformationGain(dataSet: List[str], max_common_features: int) -> int:
    n = len(dataSet)
    counts = []
    lengths = []
    for s in dataSet:
        c = [0] * 26
        for ch in s:
            c[ord(ch) - 97] += 1
        counts.append(c)
        lengths.append(len(s))

    order = sorted(range(n), key=lambda i: lengths[i])
    best = 0
    for a in range(n):
        i = order[a]
        for b in range(n - 1, a, -1):
            j = order[b]
            gain = lengths[j] - lengths[i]
            if gain <= best:
                break
            ci = counts[i]
            cj = counts[j]
            common = 0
            for k in range(26):
                x = ci[k]
                y = cj[k]
                common += x if x < y else y
                if common > max_common_features:
                    break
            if common <= max_common_features:
                best = gain
                break
    return best

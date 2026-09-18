# Group indices by message; a status is isolated iff both neighbors in its own
# message's (sorted) timestamp list are at least 10 seconds away.
from typing import List, Optional, Any
from collections import defaultdict


def showIsolatedMessages(timestamps: List[int], messages: List[str]) -> List[str]:
    groups = defaultdict(list)
    for i, m in enumerate(messages):
        groups[m].append(i)

    isolated = [False] * len(timestamps)
    for m, idxs in groups.items():
        for k, i in enumerate(idxs):
            t = timestamps[i]
            ok = True
            if k > 0 and t - timestamps[idxs[k - 1]] < 10:
                ok = False
            if ok and k + 1 < len(idxs) and timestamps[idxs[k + 1]] - t < 10:
                ok = False
            isolated[i] = ok

    return [
        "[" + str(timestamps[i]) + "s] " + messages[i]
        for i in range(len(timestamps))
        if isolated[i]
    ]

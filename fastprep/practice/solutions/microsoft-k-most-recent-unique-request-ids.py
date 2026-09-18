# Right-to-left scan with a seen-set, stopping after k distinct ids.
from typing import List, Optional, Any


def getMostRecentUniqueRequests(requests: List[str], k: int) -> List[str]:
    seen = set()
    result = []
    for i in range(len(requests) - 1, -1, -1):
        rid = requests[i]
        if rid in seen:
            continue
        seen.add(rid)
        result.append(rid)
        if len(result) == k:
            break
    return result

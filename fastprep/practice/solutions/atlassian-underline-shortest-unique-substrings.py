# Sweep substring lengths in increasing order; per length count how many strings contain each
# lowercased substring, and the first position whose substring is owned by exactly one string wins.
from typing import List, Optional, Any


def underlineShortestUniqueSubstrings(strings: List[str]) -> List[str]:
    n = len(strings)
    lower = [s.lower() for s in strings]
    result = list(strings)
    pending = set(range(n))
    max_len = max((len(s) for s in strings), default=0)

    for length in range(1, max_len + 1):
        if not pending:
            break
        # how many distinct strings contain each substring of this length
        owners = {}
        for i, s in enumerate(lower):
            seen = set()
            for start in range(len(s) - length + 1):
                sub = s[start:start + length]
                if sub in seen:
                    continue
                seen.add(sub)
                owners[sub] = owners.get(sub, 0) + 1
        resolved = []
        for i in sorted(pending):
            s = lower[i]
            for start in range(len(s) - length + 1):
                if owners.get(s[start:start + length]) == 1:
                    original = strings[i]
                    result[i] = (original[:start] + "<u>" +
                                 original[start:start + length] + "</u>" +
                                 original[start + length:])
                    resolved.append(i)
                    break
        pending.difference_update(resolved)

    return result

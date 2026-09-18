# Locate the flagged endpoints, then hash-set check that every integer in the inclusive range is present.
from typing import List


def completeFlaggedRange(values: List[int], startFlags: List[bool], endFlags: List[bool]) -> List[int]:
    start = end = None
    for i, v in enumerate(values):
        if startFlags[i]:
            start = v
        if endFlags[i]:
            end = v
    if start is None or end is None:
        return []
    present = set(values)
    for x in range(start, end + 1):
        if x not in present:
            return []
    return list(range(start, end + 1))

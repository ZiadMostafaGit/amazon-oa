# Hash-set incremental group count: deleting a house splits, keeps, or removes a group.
from typing import List, Optional, Any


def neighboringHouseGroups(houses: List[int], instructions: List[int]) -> List[int]:
    present = set(houses)
    # A group's count equals the number of houses with no left neighbor present.
    groups = 0
    for h in present:
        if h - 1 not in present:
            groups += 1

    out = []
    for x in instructions:
        if x not in present:
            out.append(groups)
            continue
        present.discard(x)
        left = (x - 1) in present
        right = (x + 1) in present
        if left and right:
            groups += 1      # the group splits in two
        elif not left and not right:
            groups -= 1      # the house was a singleton group
        out.append(groups)
    return out

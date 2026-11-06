# Insertions needed = len(finalList) - LCS(finalList, initialList). finalList has unique values, so map
# each initialList value to its index in finalList and the LCS becomes a longest increasing subsequence.
from bisect import bisect_left
from typing import List


def minimumInsertions(finalList: List[int], initialList: List[int]) -> int:
    pos = {v: i for i, v in enumerate(finalList)}
    tails = []
    for v in initialList:
        if v in pos:
            p = pos[v]
            k = bisect_left(tails, p)
            if k == len(tails):
                tails.append(p)
            else:
                tails[k] = p
    return len(finalList) - len(tails)

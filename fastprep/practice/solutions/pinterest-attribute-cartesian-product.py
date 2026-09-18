# Iterative Cartesian product: extend the prefix list attribute by attribute, left to right.
from typing import List


def expandAttributeCombinations(keys: List[str], values: List[List[str]]) -> List[List[str]]:
    rows = [[]]
    for i in range(len(keys)):
        opts = values[i]
        if not opts:
            return []
        nxt = []
        for row in rows:
            for v in opts:
                nxt.append(row + [v])
        rows = nxt
    return rows

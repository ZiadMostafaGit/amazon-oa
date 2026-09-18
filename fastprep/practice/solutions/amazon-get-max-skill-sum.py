# Prefix sums keyed by expertise balance (+1 developer, -1 marketer); keep min skill prefix per balance.
from typing import Dict, List


def getMaxSkillSum(expertise: List[int], skill: List[int]) -> int:
    best = 0
    balance = 0
    total = 0
    first: Dict[int, int] = {0: 0}
    for e, s in zip(expertise, skill):
        balance += 1 if e == 1 else -1
        total += s
        if balance in first:
            cand = total - first[balance]
            if cand > best:
                best = cand
            if total < first[balance]:
                first[balance] = total
        else:
            first[balance] = total
    return best

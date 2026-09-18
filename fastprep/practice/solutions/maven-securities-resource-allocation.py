# Greedy: each row's minimum reachable sum is its nonzero sum plus one per zero; answer is the max, if both rows can reach it.
from typing import List, Optional, Any


def minimumResources(storageA: List[int], storageB: List[int]) -> int:
    sumA = sum(storageA)
    zerosA = storageA.count(0)
    sumB = sum(storageB)
    zerosB = storageB.count(0)
    minA = sumA + zerosA
    minB = sumB + zerosB
    target = max(minA, minB)
    if zerosA == 0 and target != sumA:
        return -1
    if zerosB == 0 and target != sumB:
        return -1
    return target

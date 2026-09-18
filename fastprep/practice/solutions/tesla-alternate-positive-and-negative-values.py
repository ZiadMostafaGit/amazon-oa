# Two stable queues (positives, negatives) interleaved, majority sign first, ties to positive.
from typing import List, Optional, Any


def alternateSigns(nums: List[int]) -> List[int]:
    pos = [x for x in nums if x > 0]
    neg = [x for x in nums if x < 0]
    if len(neg) > len(pos):
        first, second = neg, pos
    else:
        first, second = pos, neg
    out = []
    for i in range(len(first)):
        out.append(first[i])
        if i < len(second):
            out.append(second[i])
    return out

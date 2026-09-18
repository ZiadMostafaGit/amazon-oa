# Direct classification: test arithmetic, then integer-ratio geometric, then Fibonacci-style, in that order.
from typing import List


def nextSeriesNumber(sequence: List[int]) -> int:
    n = len(sequence)

    d = sequence[1] - sequence[0]
    if all(sequence[i] - sequence[i - 1] == d for i in range(1, n)):
        return sequence[-1] + d

    r = None
    ok = True
    for i in range(1, n):
        prev, cur = sequence[i - 1], sequence[i]
        if prev == 0:
            if cur != 0:
                ok = False
                break
            continue
        if cur % prev != 0:
            ok = False
            break
        cand = cur // prev
        if r is None:
            r = cand
        elif r != cand:
            ok = False
            break
    if ok and r is not None:
        # every step must be consistent with the single multiplier r
        if all(sequence[i] == sequence[i - 1] * r for i in range(1, n)):
            return sequence[-1] * r

    if all(sequence[i] == sequence[i - 1] + sequence[i - 2] for i in range(2, n)):
        return sequence[-1] + sequence[-2]

    return -999

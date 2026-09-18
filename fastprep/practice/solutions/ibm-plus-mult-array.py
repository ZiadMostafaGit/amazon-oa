# Evaluate each index-parity subsequence left to right under mod 2 arithmetic.
from typing import List, Optional, Any


def _evaluate_mod2(values: List[int]) -> int:
    if not values:
        return 0
    result = values[0] % 2
    multiply = True
    for value in values[1:]:
        term = value % 2
        if multiply:
            result = (result * term) % 2
        else:
            result = (result + term) % 2
        multiply = not multiply
    return result % 2


def plusMultArray(A: List[int]) -> str:
    r_even = _evaluate_mod2(A[0::2])
    r_odd = _evaluate_mod2(A[1::2])
    if r_odd > r_even:
        return "ODD"
    if r_even > r_odd:
        return "EVEN"
    return "NEUTRAL"

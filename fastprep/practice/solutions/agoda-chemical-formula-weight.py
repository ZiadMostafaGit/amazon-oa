# Single-pass tokenizer over the flat formula, accumulating weight * count per term.
from typing import List, Optional, Any


def formulaWeight(formula: str, elements: List[str], weights: List[int]) -> int:
    table = {e: w for e, w in zip(elements, weights)}
    total = 0
    i = 0
    n = len(formula)
    while i < n:
        if not formula[i].isupper():
            i += 1
            continue
        j = i + 1
        while j < n and formula[j].islower():
            j += 1
        symbol = formula[i:j]
        k = j
        while k < n and formula[k].isdigit():
            k += 1
        count = int(formula[j:k]) if k > j else 1
        total += table.get(symbol, 0) * count
        i = k
    return total

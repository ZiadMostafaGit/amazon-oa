# Brute-force over all 2^(n-1) operator masks, evaluating with multiplication precedence.
from typing import List, Optional, Any


def findExpressions(numbers: List[int], target: int) -> List[str]:
    n = len(numbers)
    if n == 0:
        return []
    if n == 1:
        return [str(numbers[0])] if numbers[0] == target else []

    results = set()
    slots = n - 1
    for mask in range(1 << slots):
        # evaluate: accumulate product of current multiplication group, sum groups
        total = 0
        prod = numbers[0]
        for i in range(slots):
            nxt = numbers[i + 1]
            if (mask >> i) & 1:  # '*'
                prod *= nxt
            else:  # '+'
                total += prod
                prod = nxt
        total += prod
        if total == target:
            parts = [str(numbers[0])]
            for i in range(slots):
                parts.append('*' if (mask >> i) & 1 else '+')
                parts.append(str(numbers[i + 1]))
            results.add(''.join(parts))
    return sorted(results)

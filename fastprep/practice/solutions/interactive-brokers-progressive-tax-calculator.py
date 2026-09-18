# Sweep brackets accumulating marginal tax on each slice of income.
from typing import List


def calculateTax(lowerCutoffs: List[int], rates: List[float], income: int) -> float:
    total = 0.0
    n = len(lowerCutoffs)
    for i in range(n):
        low = lowerCutoffs[i]
        if income <= low:
            break
        high = lowerCutoffs[i + 1] if i + 1 < n else income
        top = high if high < income else income
        total += (top - low) * rates[i]
    return total

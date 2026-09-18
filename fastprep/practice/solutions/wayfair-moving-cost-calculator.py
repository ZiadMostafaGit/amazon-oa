# Direct accumulation: sum volume * rate over all packages.
from typing import List


def calculateMovingCost(packages: List[List[int]], categoryRates: List[int]) -> int:
    total = 0
    for cat, length, width, height in packages:
        total += length * width * height * categoryRates[cat]
    return total

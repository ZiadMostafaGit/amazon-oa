from typing import List, Optional, Any


def maximizeProtectedPopulation(population: List[int], unit: str) -> int:
    NEG = float("-inf")
    # cov = best total of finalized cities 0..i-2 when city i-1 is covered / not covered
    cov, unc = NEG, 0
    for i, p in enumerate(population):
        prev = population[i - 1] if i > 0 else 0
        if unit[i] == "1":
            # stay: city i covered, finalize i-1 with its own state
            stay = max(cov + prev, unc)
            # move left (only if i > 0): finalize i-1 as covered, city i not covered
            move = max(cov, unc) + prev if i > 0 else NEG
            cov, unc = stay, move
        else:
            cov, unc = NEG, max(cov + prev, unc)
    last = population[-1] if population else 0
    return max(cov + last, unc)

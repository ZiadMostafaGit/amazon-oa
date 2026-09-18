# Each value can only be replaced by an original array value dividing it: take the smallest such divisor.
from typing import List


def determineMinimalExpense(expense: List[int]) -> int:
    if not expense:
        return 0
    uniq = sorted(set(expense))
    max_val = uniq[-1]
    best = {}
    if len(uniq) * len(uniq) <= max_val + len(uniq):
        # Pairwise over distinct values: first (smallest) divisor wins.
        for x in uniq:
            for d in uniq:
                if d > x:
                    break
                if x % d == 0:
                    best[x] = d
                    break
    else:
        # Sieve: for each distinct value ascending, stamp its multiples that are present.
        present = set(uniq)
        for d in uniq:
            for m in range(d, max_val + 1, d):
                if m in present and m not in best:
                    best[m] = d
    return sum(best[x] for x in expense)

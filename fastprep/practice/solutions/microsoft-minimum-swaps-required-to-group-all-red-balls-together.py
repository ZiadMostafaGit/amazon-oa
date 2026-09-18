# Normalize red positions by their target offsets, then gather them at the median.
def minSwaps(colors: str) -> int:
    pos = [i - j for j, i in enumerate(i for i, ch in enumerate(colors) if ch == 'R')]
    if len(pos) <= 1:
        return 0
    median = pos[len(pos) // 2]
    total = 0
    for p in pos:
        total += p - median if p > median else median - p
        if total > 1_000_000_000:
            return -1
    return total

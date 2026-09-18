# Per divisor closed form: full cycles of 0..b-1 plus a partial cycle prefix.
def sumRemainders(i: int, j: int) -> int:
    n = i + 1
    total = 0
    for b in range(1, j + 1):
        q, r = divmod(n, b)
        total += q * (b * (b - 1) // 2) + r * (r - 1) // 2
    return total

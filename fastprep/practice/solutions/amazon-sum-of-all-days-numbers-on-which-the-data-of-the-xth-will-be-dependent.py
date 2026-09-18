# Divisor-block enumeration: sum the distinct values of floor(n/k) over all k >= 1 (0 included).
def sumOfAllDaysNumbers(n: int) -> int:
    if n <= 0:
        return 0
    seen = set()
    k = 1
    while k <= n:
        q = n // k
        seen.add(q)
        k = n // q + 1
    seen.add(0)  # k = n + 1 and beyond give floor(n/k) = 0
    return sum(seen)

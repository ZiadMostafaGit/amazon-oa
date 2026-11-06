# Euclid: gcd(a, b) = gcd(b, a mod b), and gcd(a, 0) = a.
def greatestCommonDivisor(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

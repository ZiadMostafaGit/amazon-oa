# The count equals the number of odd divisors of num minus one (found by factorizing the odd part).
def consecutive(num: int) -> int:
    n = num
    while n % 2 == 0:
        n //= 2
    divisors = 1
    p = 3
    while p * p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            divisors *= (e + 1)
        p += 2
    if n > 1:
        divisors *= 2
    return divisors - 1

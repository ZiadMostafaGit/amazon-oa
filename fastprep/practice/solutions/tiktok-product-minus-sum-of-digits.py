# Single pass over decimal digits accumulating product and sum.
def subtractProductAndSum(n: int) -> int:
    product = 1
    total = 0
    m = abs(n)
    if m == 0:
        return 0
    while m > 0:
        d = m % 10
        product *= d
        total += d
        m //= 10
    return product - total

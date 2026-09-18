# Single pass over the decimal digits accumulating product and sum.
def subtractProductAndSum(n: int) -> int:
    product = 1
    total = 0
    for ch in str(n):
        d = int(ch)
        product *= d
        total += d
    return product - total

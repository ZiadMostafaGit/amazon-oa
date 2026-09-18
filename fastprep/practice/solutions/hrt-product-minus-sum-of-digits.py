# Single pass over the decimal digits accumulating product and sum.
def solution(n: int) -> int:
    product = 1
    total = 0
    for ch in str(n):
        d = ord(ch) - 48
        product *= d
        total += d
    return product - total

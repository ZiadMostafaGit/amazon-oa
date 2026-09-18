# Digital root: repeated digit sums collapse to num mod 9 (with 9 for nonzero multiples of 9).
def addDigits(num: int) -> int:
    if num == 0:
        return 0
    r = num % 9
    return 9 if r == 0 else r

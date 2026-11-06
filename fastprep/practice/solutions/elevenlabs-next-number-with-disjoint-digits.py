def nextDisjointDigitNumber(n: int) -> int:
    s = str(n)
    allowed = sorted(set("0123456789") - set(s))
    LIMIT = 2 ** 31 - 1
    if not allowed:
        return -1
    lo = allowed[0]
    nonzero = [d for d in allowed if d != "0"]
    if not nonzero:
        return -1
    L = len(s)
    # same length: every digit of n is forbidden, so the first digit must exceed s[0]
    bigger = [d for d in nonzero if d > s[0]]
    if bigger:
        cand = int(bigger[0] + lo * (L - 1))
    else:
        cand = int(nonzero[0] + lo * L)
    return cand if cand <= LIMIT else -1

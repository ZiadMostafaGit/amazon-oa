# Binary search on the block index using closed-form prefix lengths.
def kthInfiniteCharacter(s: str, t: str, k: int) -> str:
    ls, lt = len(s), len(t)

    def total(m: int) -> int:
        # total length of the first m blocks
        o = (m + 1) // 2          # count of odd-indexed blocks
        e = m // 2                # count of even-indexed blocks
        return ls * o * o + lt * e * (e + 1)

    lo, hi = 1, 1
    while total(hi) < k:
        hi *= 2
    while lo < hi:
        mid = (lo + hi) // 2
        if total(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    m = lo
    offset = k - total(m - 1) - 1   # 0-indexed position inside block m
    base = s if m % 2 == 1 else t
    return base[offset % len(base)]

# Generate the strictly increasing sequence, then two-pointer count of ordered pairs with product <= a.
from array import array


def variantsCount(n: int, s0: int, k: int, b: int, m: int, a: int) -> int:
    s = array('q', bytes(8 * n))
    cur = s0
    s[0] = cur
    for i in range(1, n):
        cur = ((k * cur + b) % m) + 1 + cur
        s[i] = cur
    total = 0
    j = n - 1
    for i in range(n):
        si = s[i]
        if si > a:
            break
        while j >= 0 and si * s[j] > a:
            j -= 1
        if j < 0:
            break
        total += j + 1
    return total

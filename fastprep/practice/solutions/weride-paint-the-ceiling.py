# Generate the strictly increasing sequence, then a monotone two-pointer counts ordered pairs with product <= a.
def paintTheCeiling(s0: int, n: int, k: int, b: int, m: int, a: int) -> int:
    s = [0] * n
    cur = s0
    s[0] = cur
    for i in range(1, n):
        cur = ((k * cur + b) % m) + 1 + cur
        s[i] = cur
    total = 0
    j = n - 1
    for i in range(n):
        si = s[i]
        while j >= 0 and si * s[j] > a:
            j -= 1
        if j < 0:
            break
        total += j + 1
    return total

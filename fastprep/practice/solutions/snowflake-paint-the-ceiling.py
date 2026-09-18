# Generate the increasing side lengths, then count ordered pairs with product <= a via two pointers.
def paintTheCeiling(s0: int, n: int, k: int, b: int, m: int, a: int) -> int:
    limit = a // s0
    s = [s0]
    cur = s0
    for _ in range(1, n):
        cur = ((k * cur + b) % m) + 1 + cur
        if cur > limit:
            break
        s.append(cur)
    size = len(s)
    count = 0
    j = size - 1
    for i in range(size):
        si = s[i]
        while j >= 0 and si * s[j] > a:
            j -= 1
        if j < 0:
            break
        count += j + 1
    return count

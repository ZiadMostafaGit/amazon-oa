# Exchange argument: an optimal filling sorts the '!' chars (0s then 1s if x<=y, else 1s then 0s);
# scan every split point with prefix sums of fixed/variable pair costs.
def minTotalErrors(errorString: str, x: int, y: int) -> int:
    n = len(errorString)
    qs = [i for i, c in enumerate(errorString) if c == '!']
    m = len(qs)

    # cost of the fully fixed part: x per "01" subsequence, y per "10" subsequence
    const = 0
    zeros = 0
    ones = 0
    for c in errorString:
        if c == '0':
            const += y * ones
            zeros += 1
        elif c == '1':
            const += x * zeros
            ones += 1

    if m == 0:
        return const

    # prefix counts of fixed 0s / 1s
    pre0 = [0] * (n + 1)
    pre1 = [0] * (n + 1)
    for i, c in enumerate(errorString):
        pre0[i + 1] = pre0[i] + (1 if c == '0' else 0)
        pre1[i + 1] = pre1[i] + (1 if c == '1' else 0)
    tot0 = pre0[n]
    tot1 = pre1[n]

    def fixed_cost(pos: int, ch: int) -> int:
        b0 = pre0[pos]
        b1 = pre1[pos]
        a0 = tot0 - b0
        a1 = tot1 - b1
        if ch == 1:
            # "01" with earlier zeros, "10" with later zeros
            return x * b0 + y * a0
        # ch == 0: "10" with earlier ones, "01" with later ones
        return y * b1 + x * a1

    if x <= y:
        a_ch, b_ch, ab_cost = 0, 1, x
    else:
        a_ch, b_ch, ab_cost = 1, 0, y

    costA = [fixed_cost(p, a_ch) for p in qs]
    costB = [fixed_cost(p, b_ch) for p in qs]

    prefA = [0] * (m + 1)
    prefB = [0] * (m + 1)
    for j in range(m):
        prefA[j + 1] = prefA[j] + costA[j]
        prefB[j + 1] = prefB[j] + costB[j]

    best = None
    for t in range(m + 1):
        total = const + prefA[t] + (prefB[m] - prefB[t]) + t * (m - t) * ab_cost
        if best is None or total < best:
            best = total
    return best

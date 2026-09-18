# Exchange argument: optimal assigns all '!' of one char before the other, then prefix sums over the split point.
MOD = 10 ** 9 + 7


def getMinErrors(errorString: str, x: int, y: int) -> int:
    n = len(errorString)
    # prefix counts of fixed '0' and '1'
    zeros_before = [0] * (n + 1)
    ones_before = [0] * (n + 1)
    for i, ch in enumerate(errorString):
        zeros_before[i + 1] = zeros_before[i] + (1 if ch == '0' else 0)
        ones_before[i + 1] = ones_before[i] + (1 if ch == '1' else 0)
    total_zeros = zeros_before[n]
    total_ones = ones_before[n]

    # cost among the fixed characters only
    base = 0
    for i, ch in enumerate(errorString):
        if ch == '1':
            base += x * zeros_before[i]
        elif ch == '0':
            base += y * ones_before[i]

    marks = [i for i, ch in enumerate(errorString) if ch == '!']
    m = len(marks)
    if m == 0:
        return base % MOD

    # cost of putting '0' / '1' at a '!' position, against the fixed characters
    cost0 = []
    cost1 = []
    for p in marks:
        z_lt, o_lt = zeros_before[p], ones_before[p]
        z_gt, o_gt = total_zeros - z_lt, total_ones - o_lt
        cost0.append(y * o_lt + x * o_gt)
        cost1.append(x * z_lt + y * z_gt)

    if x <= y:
        first, second = cost0, cost1   # zeros come before ones
        pair_cost = x
    else:
        first, second = cost1, cost0   # ones come before zeros
        pair_cost = y

    pre_first = [0] * (m + 1)
    suf_second = [0] * (m + 1)
    for i in range(m):
        pre_first[i + 1] = pre_first[i] + first[i]
    for i in range(m - 1, -1, -1):
        suf_second[i] = suf_second[i + 1] + second[i]

    best = None
    for k in range(m + 1):
        total = base + pre_first[k] + suf_second[k] + pair_cost * k * (m - k)
        if best is None or total < best:
            best = total
    return best % MOD

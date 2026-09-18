# Pick k smallest '(' indices and k largest ')' indices via prefix sums; k bounded by greedy max matching.
def maximumScoreInBalancedString(s: str) -> int:
    opens = [i for i, c in enumerate(s) if c == '(']
    closes = [i for i, c in enumerate(s) if c == ')']

    # greedy maximum number of matchable pairs
    kmax = 0
    avail = 0
    for c in s:
        if c == '(':
            avail += 1
        elif avail > 0:
            avail -= 1
            kmax += 1
    kmax = min(kmax, len(opens), len(closes))

    best = 0
    open_sum = 0
    close_sum = 0
    for k in range(1, kmax + 1):
        open_sum += opens[k - 1]
        close_sum += closes[len(closes) - k]
        val = close_sum - open_sum
        if val > best:
            best = val
    return best

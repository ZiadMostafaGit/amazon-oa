# Josephus elimination with the count offset by the virus start position, using the batched O(k log n) recurrence.
def _josephus(n: int, k: int) -> int:
    # 0-indexed survivor when counting starts at position 0 and every k-th node is removed
    if k == 1:
        return n - 1
    res = 0
    i = 2
    while i <= n:
        if res + k < i:
            # J(i) = res + k without wrapping; batch every consecutive step that also stays below i
            steps = (i - 2 - res) // (k - 1)
            if steps > n - i + 1:
                steps = n - i + 1
            if steps < 1:
                steps = 1
            res += steps * k
            i += steps
        else:
            res = (res + k) % i
            i += 1
    return res


def findLastAffectedSystem(numSystem: int, count: int) -> int:
    n = numSystem
    if n == 1:
        return 0
    k = count
    # the virus sits on the Kth system, so counting for each strike resumes at id k
    return (_josephus(n, k) + k) % n

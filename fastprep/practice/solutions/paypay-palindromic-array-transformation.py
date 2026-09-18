# DP over split boundaries: each boundary shifts by at most 1, and array palindrome forces b[t] + b[n-t] == L.
from typing import List


def solution(arr: List[str]) -> int:
    n = len(arr)
    if n == 1:
        return 1
    S = "".join(arr)
    L = len(S)
    P = [0] * (n + 1)
    for i, s in enumerate(arr):
        P[i + 1] = P[i] + len(s)
    K = n // 2
    cur = {0}
    for t in range(1, K + 1):
        mt = n - t
        nxt = set()
        for b in (P[t] - 1, P[t], P[t] + 1):
            if b < 0 or b > L:
                continue
            bm = L - b
            if mt == t:
                if bm != b:
                    continue
            else:
                if bm not in (P[mt] - 1, P[mt], P[mt] + 1):
                    continue
            if b > bm:
                continue
            for pb in cur:
                if pb <= b and S[pb:b] == S[L - b:L - pb]:
                    nxt.add(b)
                    break
        cur = nxt
        if not cur:
            return 0
    return 1

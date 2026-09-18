# Fenwick tree for live-element distances plus a two-state DP: each equal-value group is
# swept to one extreme then the other, and both possible finishing ends are carried forward.
from bisect import bisect_left, bisect_right
from typing import List, Optional, Any


class _Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.t = [0] * (n + 1)
        for i in range(1, n + 1):          # build with every position alive
            self.t[i] += 1
            j = i + (i & -i)
            if j <= n:
                self.t[j] += self.t[i]

    def add(self, i: int, d: int) -> None:
        i += 1
        while i <= self.n:
            self.t[i] += d
            i += i & -i

    def pref(self, i: int) -> int:         # count alive in [0, i]
        i += 1
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s

    def rng(self, a: int, b: int) -> int:
        if a > b:
            return 0
        return self.pref(b) - (self.pref(a - 1) if a else 0)


def minimumEraseOperations(arr: List[int]) -> int:
    n = len(arr)
    groups = {}
    for i, v in enumerate(arr):
        groups.setdefault(v, []).append(i)

    fen = _Fenwick(n)
    # pointer position -> cheapest number of moves to have reached that state
    states = {0: 0}
    for v in sorted(groups):
        mem = groups[v]              # already ascending
        g1, gk, k = mem[0], mem[-1], len(mem)
        span = fen.rng(g1, gk) - k   # crossing the group's span once, erasing as we go

        nxt = {}
        for pos, cost in states.items():
            lo_g1, hi_g1 = (pos, g1) if pos <= g1 else (g1, pos)
            lo_gk, hi_gk = (pos, gk) if pos <= gk else (gk, pos)
            # every group member crossed is erased on the spot, which advances for free
            to_g1 = fen.rng(lo_g1, hi_g1) - (bisect_right(mem, hi_g1) - bisect_left(mem, lo_g1))
            to_gk = fen.rng(lo_gk, hi_gk) - (bisect_right(mem, hi_gk) - bisect_left(mem, lo_gk))
            # leftmost end first, then sweep right (ends at gk unless the sweep passed it)
            a_cost, a_end = (cost + to_g1 + span, gk) if pos < gk else (cost + to_g1, g1)
            # rightmost end first, then sweep left
            b_cost, b_end = (cost + to_gk + span, g1) if pos > g1 else (cost + to_gk, gk)
            if a_cost < nxt.get(a_end, a_cost + 1):
                nxt[a_end] = a_cost
            if b_cost < nxt.get(b_end, b_cost + 1):
                nxt[b_end] = b_cost
        states = nxt
        for i in mem:
            fen.add(i, -1)
    return min(states.values()) + n

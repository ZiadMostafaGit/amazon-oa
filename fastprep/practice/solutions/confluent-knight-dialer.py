# DP over keypad adjacency: counts per digit iterated n-1 times, mod 1e9+7.
MOD = 1000000007

MOVES = {
    0: [4, 6],
    1: [6, 8],
    2: [7, 9],
    3: [4, 8],
    4: [3, 9, 0],
    5: [],
    6: [1, 7, 0],
    7: [2, 6],
    8: [1, 3],
    9: [2, 4],
}


def countKnightDialerNumbers(n: int) -> int:
    cur = [1] * 10
    for _ in range(n - 1):
        nxt = [0] * 10
        for d in range(10):
            c = cur[d]
            if c:
                for t in MOVES[d]:
                    nxt[t] = (nxt[t] + c) % MOD
        cur = nxt
    return sum(cur) % MOD

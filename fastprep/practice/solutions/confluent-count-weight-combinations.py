def countWeightCombinations(total: int, k: int) -> int:
    MOD = 10 ** 9 + 7
    ways = [0] * (total + 1)
    ways[0] = 1
    for w in range(1, min(k, total) + 1):
        for s in range(w, total + 1):
            ways[s] = (ways[s] + ways[s - w]) % MOD
    return ways[total]

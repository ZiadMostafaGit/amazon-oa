# Sliding window over the two alternating target patterns, counting flips needed.
def getMaxAlternatingMusic(music: str, k: int) -> int:
    n = len(music)
    if n == 0:
        return 0

    best = 0
    for start_bit in (0, 1):
        left = 0
        cost = 0
        for right in range(n):
            expected = str((right + start_bit) & 1)
            if music[right] != expected:
                cost += 1
            while cost > k:
                exp_l = str((left + start_bit) & 1)
                if music[left] != exp_l:
                    cost -= 1
                left += 1
            if right - left + 1 > best:
                best = right - left + 1
    return best

# Approach: for each length-k block, count mismatched mirrored character pairs.
def minChangesForPalindromicBlocks(password: str, k: int) -> int:
    total = 0
    n = len(password)
    for start in range(0, n, k):
        i, j = start, start + k - 1
        while i < j:
            if password[i] != password[j]:
                total += 1
            i += 1
            j -= 1
    return total

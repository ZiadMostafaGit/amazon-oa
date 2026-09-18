# Prefix sums over encrypted-only scores; slide a window of length k for the best gain.
from typing import List, Optional, Any


def maximumDecryptedScore(scores: List[int], decryptionStatus: List[int], k: int) -> int:
    n = len(scores)
    base = 0
    pref = [0] * (n + 1)
    for i in range(n):
        if decryptionStatus[i] == 1:
            base += scores[i]
            pref[i + 1] = pref[i]
        else:
            pref[i + 1] = pref[i] + scores[i]

    best = 0
    width = min(k, n)
    for start in range(0, n - width + 1):
        gain = pref[start + width] - pref[start]
        if gain > best:
            best = gain
    return base + best

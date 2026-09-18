# Sliding window over word tokens with a need-count map (minimum window substring on words).
from typing import List, Optional, Any
from collections import Counter


def minimumRequiredWordWindow(text: str, requiredWords: List[str]) -> str:
    words = text.split()
    if not words or not requiredWords:
        return ""
    need = Counter(requiredWords)
    missing = len(requiredWords)
    have = Counter()
    best_l, best_r = -1, -1
    left = 0
    for right, w in enumerate(words):
        if need.get(w, 0) > 0:
            if have[w] < need[w]:
                missing -= 1
            have[w] += 1
        while missing == 0:
            if best_l == -1 or (right - left) < (best_r - best_l):
                best_l, best_r = left, right
            lw = words[left]
            if need.get(lw, 0) > 0:
                have[lw] -= 1
                if have[lw] < need[lw]:
                    missing += 1
            left += 1
    if best_l == -1:
        return ""
    return " ".join(words[best_l:best_r + 1])

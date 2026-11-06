# Count equal pairs, plus (word, proper suffix) pairs via a frequency map. O(n * L^2).
from collections import Counter
from typing import List, Optional, Any


def solution(words: List[str]) -> int:
    cnt = Counter(words)
    total = 0
    for w, c in cnt.items():
        total += c * (c - 1) // 2
        for k in range(1, len(w)):
            s = w[k:]
            if s in cnt:
                total += c * cnt[s]
    return total

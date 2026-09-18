# Group wordSet by sorted-letter signature; each sentence's answer is the product of group sizes.
from collections import Counter
from typing import List, Optional, Any


def countSentences(wordSet: List[str], sentences: List[str]) -> List[int]:
    groups = Counter("".join(sorted(w)) for w in wordSet)
    res = []
    for sentence in sentences:
        total = 1
        for word in sentence.split():
            total *= groups.get("".join(sorted(word)), 0)
            if total == 0:
                break
        res.append(total)
    return res

# Tokenize each document and scan for the phrase token list as a contiguous sublist.
from typing import List, Optional, Any


def findDocumentsWithPhrase(documents: List[str], phrase: str) -> List[int]:
    pat = phrase.split()
    m = len(pat)
    res = []
    if m == 0:
        return list(range(len(documents)))
    for i, doc in enumerate(documents):
        words = doc.split()
        n = len(words)
        for j in range(n - m + 1):
            if words[j:j + m] == pat:
                res.append(i)
                break
    return res

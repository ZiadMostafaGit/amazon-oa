# Tokenize each document into a set and test exact membership of the query word.
from typing import List, Optional, Any


def findDocumentsWithWord(documents: List[str], word: str) -> List[int]:
    result = []
    for i, doc in enumerate(documents):
        if word in set(doc.split(' ')):
            result.append(i)
    return result

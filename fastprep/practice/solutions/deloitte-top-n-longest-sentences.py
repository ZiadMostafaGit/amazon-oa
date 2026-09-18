# Stable sort by descending length (Python's sort keeps original order for ties), take n.
from typing import List, Optional, Any


def topLongestSentences(sentences: List[str], n: int) -> List[str]:
    order = sorted(range(len(sentences)), key=lambda i: -len(sentences[i]))
    return [sentences[i] for i in order[:n]]

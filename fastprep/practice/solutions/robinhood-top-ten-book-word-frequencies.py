# Regex tokenization + hash-map counting, then sort by (-frequency, word).
import re
from collections import Counter
from typing import List, Optional, Any


def topTenWords(text: str) -> List[str]:
    words = re.findall(r"[A-Za-z0-9]+", text)
    counts = Counter(w.lower() for w in words)
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ["%s %d" % (w, c) for w, c in ordered[:10]]

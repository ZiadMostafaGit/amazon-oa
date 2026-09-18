# Term-frequency embeddings with exact rational cosine comparison for stable ties.
from typing import List, Optional, Any
from collections import Counter
from fractions import Fraction


def processVectorIndex(operations: List[str], ids: List[str], texts: List[str], ks: List[int]) -> List[List[str]]:
    store = {}
    out = []
    for op, rid, text, k in zip(operations, ids, texts, ks):
        if op == "UPSERT":
            tf = Counter(text.lower().split(" "))
            norm2 = sum(c * c for c in tf.values())
            store[rid] = (tf, norm2)
            out.append([])
        else:
            qtf = Counter(text.lower().split(" "))
            qnorm2 = sum(c * c for c in qtf.values())
            scored = []
            for key, (tf, norm2) in store.items():
                dot = 0
                if len(qtf) <= len(tf):
                    for t, c in qtf.items():
                        if t in tf:
                            dot += c * tf[t]
                else:
                    for t, c in tf.items():
                        if t in qtf:
                            dot += c * qtf[t]
                # cosine is nonnegative, so compare its square exactly
                sim2 = Fraction(dot * dot, norm2 * qnorm2) if (norm2 and qnorm2) else Fraction(0)
                scored.append((-sim2, key))
            scored.sort()
            out.append([key for _, key in scored[:k]])
    return out

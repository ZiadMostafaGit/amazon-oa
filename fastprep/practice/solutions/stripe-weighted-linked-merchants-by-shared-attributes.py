# Hash-map scoring: index target's (name,value) pairs, accumulate weights per merchant, sort by (-score, id).
from typing import List, Optional, Any


def rankLinkedMerchants(merchants: List[List[str]], attributeWeights: List[str], targetMerchantId: str) -> List[str]:
    weights = {}
    for entry in attributeWeights:
        idx = entry.rfind("|")
        if idx < 0:
            continue
        weights[entry[:idx]] = int(entry[idx + 1:])

    target_attrs = {}
    for row in merchants:
        if row and row[0] == targetMerchantId:
            for i in range(1, len(row) - 1, 2):
                target_attrs[(row[i], row[i + 1])] = weights.get(row[i], 0)
            break

    results = []
    for row in merchants:
        if not row or row[0] == targetMerchantId:
            continue
        score = 0
        for i in range(1, len(row) - 1, 2):
            score += target_attrs.get((row[i], row[i + 1]), 0)
        if score > 0:
            results.append((-score, row[0], score))

    results.sort(key=lambda t: (t[0], t[1]))
    return ["%s|%d" % (mid, sc) for _, mid, sc in results]

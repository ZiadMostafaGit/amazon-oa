# Three sequential left-to-right passes over the transactions with hash maps keyed by (customer, merchant[, hour]).
from typing import List, Optional, Any


def calculateMerchantFraudScores(transactions: List[List[str]], merchantIds: List[str], baseScores: List[int], rules: List[List[int]]) -> List[int]:
    index = {m: i for i, m in enumerate(merchantIds)}
    score = list(baseScores)

    # Pass 1: amount threshold -> multiplicative factor.
    for t, r in zip(transactions, rules):
        amount = int(t[3])
        if amount > r[0]:
            score[index[t[1]]] *= r[1]

    # Pass 2: repeat customer-merchant pairs.
    seen = {}
    for t, r in zip(transactions, rules):
        key = (t[0], t[1])
        bucket = seen.setdefault(key, [])
        if len(bucket) < 3:
            bucket.append(r[2])
            if len(bucket) == 3:
                score[index[t[1]]] += bucket[0] + bucket[1] + bucket[2]
        else:
            score[index[t[1]]] += r[2]

    # Pass 3: same-hour penalties, signed by the hour window.
    groups = {}
    for t, r in zip(transactions, rules):
        hour = int(t[2])
        if 12 <= hour <= 17:
            sign = 1
        elif 9 <= hour <= 11 or 18 <= hour <= 21:
            sign = -1
        else:
            sign = 0
        key = (t[0], t[1], hour)
        bucket = groups.setdefault(key, [])
        if len(bucket) < 3:
            bucket.append(r[3])
            if len(bucket) == 3 and sign:
                score[index[t[1]]] += sign * (bucket[0] + bucket[1] + bucket[2])
        elif sign:
            score[index[t[1]]] += sign * r[3]

    return score

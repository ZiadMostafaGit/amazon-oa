# Linear scan over all variations, comparing price/weight ratios as exact cross-multiplied fractions.
from typing import List


def costliestChocolate(brand: str, recordBrands: List[str], productNumbers: List[int], prices: List[List[int]], weights: List[List[int]]) -> int:
    best_num = -1  # best ratio numerator (price)
    best_den = 1   # best ratio denominator (weight)
    best_id = -1

    for i, b in enumerate(recordBrands):
        if b != brand:
            continue
        pi = prices[i]
        wi = weights[i]
        # best ratio within this chocolate
        cur_num = -1
        cur_den = 1
        for j in range(len(pi)):
            p = pi[j]
            w = wi[j]
            if cur_num < 0 or p * cur_den > cur_num * w:
                cur_num = p
                cur_den = w
        if cur_num < 0:
            continue
        pid = productNumbers[i]
        if best_id < 0:
            best_num, best_den, best_id = cur_num, cur_den, pid
        else:
            lhs = cur_num * best_den
            rhs = best_num * cur_den
            if lhs > rhs or (lhs == rhs and pid < best_id):
                best_num, best_den, best_id = cur_num, cur_den, pid

    return best_id

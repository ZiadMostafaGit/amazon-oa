# Group items by (item-discount, category-discount) pair, precompute the 4 rounded sums per group,
# then enumerate the <=4 affordable category subsets and greedily take the best-gain item discounts.
from typing import List, Optional, Any
from itertools import combinations

BUDGET = 20
ITEM_COST = 2
CAT_COST = 5
CAP = 8000  # 80% expressed in ten-thousandths


def _rounded(price: int, num: int) -> int:
    # round half to even of price * num / 10000 using exact integers
    if num <= 0 or price == 0:
        return 0
    q, r = divmod(price * num, 10000)
    if r * 2 > 10000 or (r * 2 == 10000 and q % 2 == 1):
        q += 1
    return q


def _num(pa: int, pb: int) -> int:
    n = 10000 - (100 - pa) * (100 - pb)
    return CAP if n > CAP else n


def optimizeDiscounts(itemNames: List[str], prices: List[int], categories: List[str],
                      discountTypes: List[str], discountNames: List[str],
                      percentOff: List[int]) -> List[int]:
    item_disc = {}
    cat_disc = {}
    for idx in range(len(discountTypes)):
        if discountTypes[idx] == "item":
            item_disc[discountNames[idx]] = idx
        else:
            cat_disc[discountNames[idx]] = idx

    # bucket items by the pair of discounts that can touch them
    buckets = {}
    for i in range(len(itemNames)):
        d = item_disc.get(itemNames[i], -1)
        c = cat_disc.get(categories[i], -1)
        if d == -1 and c == -1:
            continue
        buckets.setdefault((d, c), []).append(prices[i])

    groups = []  # (d, c, s00, s10, s01, s11)
    used_cats = set()
    for (d, c), plist in buckets.items():
        pa = percentOff[d] if d != -1 else 0
        pb = percentOff[c] if c != -1 else 0
        n10 = _num(pa, 0) if d != -1 else 0
        n01 = _num(0, pb) if c != -1 else 0
        n11 = _num(pa, pb)
        s10 = s01 = s11 = 0
        for p in plist:
            if d != -1:
                s10 += _rounded(p, n10)
            if c != -1:
                s01 += _rounded(p, n01)
            s11 += _rounded(p, n11)
        groups.append((d, c, 0, s10, s01, s11))
        if c != -1:
            used_cats.add(c)

    cat_list = sorted(used_cats)
    max_cats = min(len(cat_list), BUDGET // CAT_COST)

    best = (0, 0, [])  # (savings, -points sense handled below, indices)
    best_savings, best_points, best_idx = 0, 0, []

    for size in range(max_cats + 1):
        for combo in combinations(cat_list, size):
            chosen_cats = set(combo)
            points_cats = size * CAT_COST
            budget_left = BUDGET - points_cats
            base = 0
            gains = {}
            for (d, c, s00, s10, s01, s11) in groups:
                if c != -1 and c in chosen_cats:
                    base += s01
                    if d != -1:
                        gains[d] = gains.get(d, 0) + (s11 - s01)
                else:
                    base += s00
                    if d != -1:
                        gains[d] = gains.get(d, 0) + (s10 - s00)
            k = budget_left // ITEM_COST
            picks = sorted((g, idx) for idx, g in gains.items() if g > 0)
            picks.sort(key=lambda t: (-t[0], t[1]))
            take = picks[:k]
            savings = base + sum(g for g, _ in take)
            points = points_cats + len(take) * ITEM_COST
            indices = sorted(list(combo) + [idx for _, idx in take])
            if (savings > best_savings
                    or (savings == best_savings and points < best_points)
                    or (savings == best_savings and points == best_points and indices < best_idx)):
                best_savings, best_points, best_idx = savings, points, indices

    return [best_points] + best_idx

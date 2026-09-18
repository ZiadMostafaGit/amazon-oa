# Count how many distinct customers bought each product, keep those with count >= K, sorted.
from typing import List, Optional, Any
from collections import defaultdict


def findMostFrequentlyPurchasedProducts(tag: List[List[int]], K: int) -> List[int]:
    customers_per_product = defaultdict(int)
    for bag in tag:
        for product in set(bag):
            customers_per_product[product] += 1
    return sorted(p for p, c in customers_per_product.items() if c >= K)

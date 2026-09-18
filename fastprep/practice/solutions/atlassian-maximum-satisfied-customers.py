# Brute force over every unordered pair of shops (<=60 shops) with set-subset checks.
from typing import List, Optional, Any


def maxSatisfiedCustomers(customers: List[List[int]], shops: List[List[int]]) -> int:
    shop_sets = [set(s) for s in shops]
    cust_sets = [set(c) for c in customers]

    best = 0
    n = len(shop_sets)
    for i in range(n):
        si = shop_sets[i]
        for j in range(i, n):
            available = si | shop_sets[j]
            count = 0
            for c in cust_sets:
                if c <= available:
                    count += 1
            if count > best:
                best = count
    return best

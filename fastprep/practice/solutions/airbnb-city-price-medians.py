# Bucket prices per city in a dict, sort each bucket, format the median exactly.
from typing import List
from collections import defaultdict


def cityPriceMedians(entries: List[str]) -> List[str]:
    buckets = defaultdict(list)
    for entry in entries:
        city, _, price = entry.rpartition(' ')
        buckets[city].append(int(price))

    out = []
    for city in sorted(buckets):
        prices = sorted(buckets[city])
        n = len(prices)
        if n % 2 == 1:
            out.append(city + "=" + str(prices[n // 2]))
        else:
            total = prices[n // 2 - 1] + prices[n // 2]
            if total % 2 == 0:
                out.append(city + "=" + str(total // 2))
            else:
                out.append(city + "=" + str(total // 2) + ".5")
    return out

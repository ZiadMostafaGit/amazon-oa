# Direct chronological simulation with a per-item active-discount quota.
from typing import List, Optional, Any


def solution(pricelist: List[str], logs: List[str]) -> int:
    price = {}
    for entry in pricelist:
        name, _, value = entry.partition(":")
        price[name.strip()] = int(value.strip())

    # item -> [discount_amount, remaining_quota]
    active = {}
    revenue = 0

    for line in logs:
        line = line.strip()
        op, _, rest = line.partition(" ")
        fields = [f.strip() for f in rest.split(",")]

        if op == "sell":
            item = fields[0]
            count = int(fields[1])
            unit = price[item]
            state = active.get(item)
            if state is not None and state[1] > 0:
                used = count if count < state[1] else state[1]
                state[1] -= used
                revenue += used * (unit - state[0]) + (count - used) * unit
            else:
                revenue += count * unit
        elif op == "discount_start":
            item = fields[0]
            active[item] = [int(fields[1]), int(fields[2])]
        elif op == "discount_end":
            item = fields[0]
            active.pop(item, None)

    return revenue

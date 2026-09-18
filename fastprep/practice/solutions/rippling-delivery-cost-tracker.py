from typing import List, Optional, Any
import heapq


def _rate_to_cents(rate: str) -> int:
    """Parse a decimal USD string with at most two fractional digits into cents."""
    s = rate.strip()
    neg = s.startswith("-")
    if neg or s.startswith("+"):
        s = s[1:]
    if "." in s:
        whole, frac = s.split(".", 1)
    else:
        whole, frac = s, ""
    frac = (frac + "00")[:2]
    cents = int(whole or "0") * 100 + int(frac or "0")
    return -cents if neg else cents


def _format(num: int) -> str:
    """num is cost measured in (cents * 3600); every judged cost is exact cents."""
    cents = num // 3600
    return "{}.{:02d}".format(cents // 100, cents % 100)


def trackDeliveryCosts(operations: List[List[str]]) -> List[str]:
    rates = {}                 # driverId -> hourly rate in cents
    total_num = 0              # total cost, scaled by 3600 cents
    unpaid_num = 0             # unpaid cost, same scale
    unpaid = []                # min-heap of (endTime, scaled cost)
    out: List[str] = []

    for op in operations or []:
        if not op:
            continue
        kind = op[0]
        if kind == "ADD_DRIVER":
            rates[op[1]] = _rate_to_cents(op[2])
        elif kind == "RECORD_DELIVERY":
            rate = rates.get(op[1], 0)
            start = int(op[2])
            end = int(op[3])
            num = rate * (end - start)
            total_num += num
            unpaid_num += num
            heapq.heappush(unpaid, (end, num))
        elif kind == "GET_TOTAL_COST":
            out.append(_format(total_num))
        elif kind == "PAY_UP_TO":
            pay_time = int(op[1])
            while unpaid and unpaid[0][0] <= pay_time:
                _end, num = heapq.heappop(unpaid)
                unpaid_num -= num
        elif kind == "GET_UNPAID_COST":
            out.append(_format(unpaid_num))
    return out

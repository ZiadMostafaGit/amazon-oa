# FIFO lot matching per ticker in integer cents, then 25% tax formatted as US currency.
from collections import deque
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional, Any


def calculateTax(trades: List[str]) -> str:
    books = {}  # ticker -> deque of [signed_shares, price_cents]; sign +1 long, -1 short
    total_profit = 0  # in cents

    for raw in trades:
        parts = raw.strip().split(",")
        ticker = parts[1].strip()
        side = parts[2].strip().upper()
        shares = int(parts[3])
        price = int((Decimal(parts[4].strip()) * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP))

        sign = 1 if side == "B" else -1
        lots = books.setdefault(ticker, deque())

        remaining = shares
        # Close opposite-signed open lots first, FIFO.
        while remaining > 0 and lots and lots[0][0] * sign < 0:
            lot = lots[0]
            open_shares = abs(lot[0])
            matched = open_shares if open_shares <= remaining else remaining
            if sign > 0:
                # buying closes a short lot: profit = short price - cover price
                total_profit += matched * (lot[1] - price)
                lot[0] += matched
            else:
                # selling closes a long lot: profit = sell price - buy price
                total_profit += matched * (price - lot[1])
                lot[0] -= matched
            remaining -= matched
            if lot[0] == 0:
                lots.popleft()

        if remaining > 0:
            lots.append([sign * remaining, price])

    tax = Decimal(total_profit) / 4 if total_profit > 0 else Decimal(0)
    tax = tax.quantize(Decimal(1), rounding=ROUND_HALF_UP)
    tax_cents = int(tax)
    dollars, cents = divmod(tax_cents, 100)
    return "${:,}.{:02d}".format(dollars, cents)

# Event simulation in integer cents: drain gift-card balances (insertion order) first, remainder to the credit card.
from typing import List, Optional, Any
from collections import deque


def _to_cents(text: str) -> int:
    text = text.strip()
    if "." in text:
        whole, frac = text.split(".")
        frac = (frac + "00")[:2]
    else:
        whole, frac = text, "00"
    sign = -1 if whole.startswith("-") else 1
    whole = whole.lstrip("+-")
    return sign * (int(whole or "0") * 100 + int(frac))


def _fmt(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return "%s%d.%02d" % (sign, cents // 100, cents % 100)


def processEvents(events: List[str]) -> List[str]:
    wallets = {}  # customer -> deque of [card_id, balance_cents]
    out: List[str] = []
    for line in events:
        parts = line.split(",")
        kind = parts[1]
        if kind == "ADD_GIFTCARD":
            customer, card_id, amount = parts[2], parts[3], _to_cents(parts[4])
            wallets.setdefault(customer, deque()).append([card_id, amount])
            out.append("")
        elif kind == "CHARGE":
            customer, amount = parts[3], _to_cents(parts[4])
            remaining = amount
            used = []
            wallet = wallets.get(customer)
            while wallet and remaining > 0:
                card_id, balance = wallet[0]
                if balance <= 0:
                    wallet.popleft()
                    continue
                take = balance if balance < remaining else remaining
                wallet[0][1] = balance - take
                remaining -= take
                used.append("%s:%s" % (card_id, _fmt(take)))
                if wallet[0][1] == 0:
                    wallet.popleft()
            out.append(",".join([_fmt(remaining)] + used))
        else:
            out.append("")
    return out

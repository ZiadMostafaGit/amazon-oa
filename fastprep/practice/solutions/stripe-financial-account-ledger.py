# Event simulation: compute each fund's settlement day from cutoff/business-day rules, then sum settled funds per query.
from typing import List, Optional, Any


def _is_business(day: int) -> bool:
    return ((day - 1) % 7) + 1 <= 5


def _next_business(day: int) -> int:
    day += 1
    while not _is_business(day):
        day += 1
    return day


def _parse_ts(token: str):
    if "," in token:
        d, h = token.split(",")
        return int(d), int(h)
    return int(token), 0


def processLedger(commands: List[str]) -> str:
    starting = {}
    settled = {}          # account -> list of (settlement_day, amount)
    ach_daily = {}        # (account, effective_day) -> accepted principal
    ach_weekly = {}       # (account, week) -> accepted principal
    results: List[str] = []

    for line in commands:
        parts = line.split()
        kind = parts[0]

        if kind == "INIT":
            acct = parts[1]
            if acct not in starting:
                starting[acct] = int(parts[2])
                settled[acct] = []

        elif kind == "FUND":
            day, hour = _parse_ts(parts[1])
            acct = parts[2]
            method = parts[3]
            amount = int(parts[4])
            if acct not in starting:
                continue

            if method == "STABLECOIN":
                settled[acct].append((day, amount))
                continue

            cutoff = 17 if method == "WIRE" else 20
            if not _is_business(day):
                eff = day
                while not _is_business(eff):
                    eff += 1
            elif hour < cutoff:
                eff = day
            else:
                eff = _next_business(day)

            if method == "WIRE":
                settled[acct].append((eff, amount))
            else:
                week = (eff - 1) // 7
                dkey = (acct, eff)
                wkey = (acct, week)
                if ach_daily.get(dkey, 0) + amount > 5_000_000:
                    continue
                if ach_weekly.get(wkey, 0) + amount > 10_000_000:
                    continue
                ach_daily[dkey] = ach_daily.get(dkey, 0) + amount
                ach_weekly[wkey] = ach_weekly.get(wkey, 0) + amount
                settled[acct].append((_next_business(eff), amount))

        elif kind == "BALANCE":
            day, _hour = _parse_ts(parts[1])
            acct = parts[2]
            if acct not in starting:
                results.append("FAILURE")
            else:
                total = starting[acct]
                for sday, amount in settled[acct]:
                    if sday <= day:
                        total += amount
                results.append(str(total))

    return ",".join(results)

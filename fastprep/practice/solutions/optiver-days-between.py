# Convert each date to a day number since a fixed epoch with a civil-calendar formula, then subtract.
def _days_from_civil(y: int, m: int, d: int) -> int:
    # Howard Hinnant's days-from-civil algorithm (proleptic Gregorian).
    y -= m <= 2
    era = (y if y >= 0 else y - 399) // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468


def daysBetween(year1: int, month1: int, day1: int, year2: int, month2: int, day2: int) -> int:
    return _days_from_civil(year2, month2, day2) - _days_from_civil(year1, month1, day1)

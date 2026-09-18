# Token parsing: strip the ordinal suffix, map the 3-letter month, reassemble as ISO YYYY-MM-DD.
from typing import List, Optional, Any

_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def preprocessDate(dates: List[str]) -> List[str]:
    out = []
    for s in dates:
        day_tok, month_tok, year_tok = s.split()
        day = int("".join(c for c in day_tok if c.isdigit()))
        month = _MONTHS[month_tok[:3].lower()]
        out.append("%s-%02d-%02d" % (year_tok, month, day))
    return out

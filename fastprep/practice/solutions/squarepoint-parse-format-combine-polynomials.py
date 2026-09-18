# Manual tokenizing parser into an exponent -> coefficient map, with int64 range checks, then canonical formatting.
from typing import List, Optional, Any

INT64_MIN = -(2 ** 63)
INT64_MAX = 2 ** 63 - 1


def _fits(v: int) -> bool:
    return INT64_MIN <= v <= INT64_MAX


def _split_terms(expr: str) -> List[str]:
    terms = []
    start = 0
    for i, ch in enumerate(expr):
        if i > 0 and (ch == '+' or ch == '-'):
            terms.append(expr[start:i])
            start = i
    terms.append(expr[start:])
    return [t for t in terms if t]


def _parse_term(term: str):
    sign = 1
    if term[0] == '+':
        term = term[1:]
    elif term[0] == '-':
        sign = -1
        term = term[1:]
    pos = term.find('x')
    if pos == -1:
        return sign * int(term), 0
    head = term[:pos]
    coef = 1 if head == '' else int(head)
    tail = term[pos + 1:]
    if tail == '':
        exp = 1
    else:
        # tail looks like ^<digits>
        exp = int(tail[1:])
    return sign * coef, exp


def combinePolynomials(polynomials: List[str]) -> str:
    acc = {}
    for expr in polynomials:
        for term in _split_terms(expr):
            coef, exp = _parse_term(term)
            if not _fits(coef):
                return "OVERFLOW"
            if exp in acc:
                total = acc[exp] + coef
                if not _fits(total):
                    return "OVERFLOW"
                acc[exp] = total
            else:
                acc[exp] = coef

    pieces = []
    for exp in sorted(acc.keys(), reverse=True):
        c = acc[exp]
        if c == 0:
            continue
        mag = abs(c)
        if not pieces:
            s = '-' if c < 0 else ''
        else:
            s = '-' if c < 0 else '+'
        if exp == 0:
            s += str(mag)
        else:
            if mag != 1:
                s += str(mag)
            s += 'x'
            if exp != 1:
                s += '^' + str(exp)
        pieces.append(s)
    if not pieces:
        return "0"
    return ''.join(pieces)

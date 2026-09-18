# Backtracking over operand splits, carrying running value and last multiplicative term.
from typing import List, Optional, Any


def addOperators(digits: str, target: int) -> List[str]:
    n = len(digits)
    res = []

    def dfs(pos: int, expr: str, value: int, last: int) -> None:
        if pos == n:
            if value == target:
                res.append(expr)
            return
        for end in range(pos + 1, n + 1):
            part = digits[pos:end]
            if len(part) > 1 and part[0] == '0':
                break
            num = int(part)
            if pos == 0:
                dfs(end, part, num, num)
            else:
                dfs(end, expr + '+' + part, value + num, num)
                dfs(end, expr + '-' + part, value - num, -num)
                dfs(end, expr + '*' + part, value - last + last * num, last * num)

    dfs(0, "", 0, 0)
    res.sort()
    return res

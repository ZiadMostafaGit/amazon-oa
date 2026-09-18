# Backtracking that always tries '(' before ')', which emits results in lexicographic order.
from typing import List, Optional, Any


def generateParenthesis(n: int) -> List[str]:
    res = []
    buf = []

    def build(open_used: int, close_used: int) -> None:
        if len(buf) == 2 * n:
            res.append("".join(buf))
            return
        if open_used < n:
            buf.append("(")
            build(open_used + 1, close_used)
            buf.pop()
        if close_used < open_used:
            buf.append(")")
            build(open_used, close_used + 1)
            buf.pop()

    build(0, 0)
    return res

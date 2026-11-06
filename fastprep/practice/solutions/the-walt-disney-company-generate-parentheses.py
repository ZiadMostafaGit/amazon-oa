from typing import List, Optional, Any


def generateParenthesis(n: int) -> List[str]:
    res = []
    buf = []

    def bt(op, cl):
        if len(buf) == 2 * n:
            res.append("".join(buf))
            return
        if op < n:
            buf.append("(")
            bt(op + 1, cl)
            buf.pop()
        if cl < op:
            buf.append(")")
            bt(op, cl + 1)
            buf.pop()

    bt(0, 0)
    return res

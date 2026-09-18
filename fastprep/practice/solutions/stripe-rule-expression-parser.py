# Hand-written lexer plus recursive-descent parser (OR < AND < NOT) emitting a canonical prefix form.
import sys
import threading


class _Bad(Exception):
    pass


_IDSTART = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")
_IDCHAR = _IDSTART | set("0123456789")
_DIGITS = set("0123456789")
_KEYWORDS = {"NOT", "AND", "OR"}


def _tokenize(s):
    toks = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c in " \t\r\n":
            i += 1
            continue
        if c in _IDSTART:
            j = i + 1
            while j < n and s[j] in _IDCHAR:
                j += 1
            word = s[i:j]
            if word in _KEYWORDS:
                toks.append((word, word))
            else:
                if len(word) > 100:
                    raise _Bad()
                toks.append(("IDENT", word))
            i = j
            continue
        if c in _DIGITS or c in "+-":
            j = i
            if c in "+-":
                j += 1
            k = j
            while k < n and s[k] in _DIGITS:
                k += 1
            if k == j:
                raise _Bad()
            toks.append(("INT", str(int(s[i:k]))))
            i = k
            continue
        if c == '"':
            j = i + 1
            out = []
            closed = False
            while j < n:
                ch = s[j]
                if ch == '"':
                    closed = True
                    j += 1
                    break
                if ch == "\\":
                    if j + 1 >= n:
                        raise _Bad()
                    nxt = s[j + 1]
                    if nxt != '"' and nxt != "\\":
                        raise _Bad()
                    out.append(nxt)
                    j += 2
                    continue
                if not (" " <= ch <= "~"):
                    raise _Bad()
                out.append(ch)
                j += 1
            if not closed:
                raise _Bad()
            text = "".join(out)
            if len(text) > 100:
                raise _Bad()
            toks.append(("STR", text))
            i = j
            continue
        if c == "(":
            toks.append(("LP", "("))
            i += 1
            continue
        if c == ")":
            toks.append(("RP", ")"))
            i += 1
            continue
        if c in "<>":
            if i + 1 < n and s[i + 1] == "=":
                toks.append(("OP", c + "="))
                i += 2
            else:
                toks.append(("OP", c))
                i += 1
            continue
        if c == "=" or c == "!":
            if i + 1 < n and s[i + 1] == "=":
                toks.append(("OP", c + "="))
                i += 2
                continue
            raise _Bad()
        raise _Bad()
    if len(toks) > 200000:
        raise _Bad()
    return toks


def _quote(text):
    out = ['"']
    for ch in text:
        if ch == '"' or ch == "\\":
            out.append("\\")
        out.append(ch)
    out.append('"')
    return "".join(out)


class _Parser(object):
    def __init__(self, toks):
        self.toks = toks
        self.pos = 0
        self.depth = 0

    def peek(self):
        if self.pos < len(self.toks):
            return self.toks[self.pos]
        return ("EOF", "")

    def parse_or(self):
        node = self.parse_and()
        while self.peek()[0] == "OR":
            self.pos += 1
            right = self.parse_and()
            node = "(OR " + node + " " + right + ")"
        return node

    def parse_and(self):
        node = self.parse_unary()
        while self.peek()[0] == "AND":
            self.pos += 1
            right = self.parse_unary()
            node = "(AND " + node + " " + right + ")"
        return node

    def parse_unary(self):
        if self.peek()[0] == "NOT":
            self.pos += 1
            return "(NOT " + self.parse_unary() + ")"
        return self.parse_primary()

    def parse_primary(self):
        kind, val = self.peek()
        if kind == "LP":
            self.pos += 1
            self.depth += 1
            if self.depth > 1000:
                raise _Bad()
            inner = self.parse_or()
            if self.peek()[0] != "RP":
                raise _Bad()
            self.pos += 1
            self.depth -= 1
            return inner
        if kind == "IDENT":
            self.pos += 1
            if self.peek()[0] != "OP":
                raise _Bad()
            op = self.toks[self.pos][1]
            self.pos += 1
            lk, lv = self.peek()
            if lk == "INT":
                lit = lv
            elif lk == "STR":
                lit = _quote(lv)
            else:
                raise _Bad()
            self.pos += 1
            return "(" + op + " " + val + " " + lit + ")"
        raise _Bad()


def _run(rule):
    toks = _tokenize(rule)
    if not toks:
        raise _Bad()
    p = _Parser(toks)
    node = p.parse_or()
    if p.pos != len(toks):
        raise _Bad()
    return node


def parseRuleExpression(rule: str) -> str:
    result = ["INVALID"]

    def work():
        try:
            result[0] = _run(rule)
        except Exception:
            result[0] = "INVALID"

    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(100000)
    try:
        threading.stack_size(64 * 1024 * 1024)
        t = threading.Thread(target=work)
        t.start()
        t.join()
    except Exception:
        work()
    finally:
        sys.setrecursionlimit(old_limit)
    return result[0]

"""Find this problem: paste a statement from anywhere, get the bank's closest.

The same question turns up under different stories and companies - Bloomberg's
"Minimum in a Rotated Sorted Array" and Goldman's copy differ in wording but
not in substance, and a statement pasted from elsewhere will wear a third
story. So no single signal is trusted. Each is good at one kind of sameness:

    examples     the pasted text contains an input/output pair the stored
                 problem has - one shared pair is close to proof;
    wording      TF-IDF cosine over the statement with the story stripped
                 (company names, stopwords), numbers kept;
    signature    the function name and parameter names, which survive a
                 rewrite almost untouched;
    constraints  the magnitudes - 10^5, 10^9 - that bound the input;
    concept      the chapters the pasted text would be filed under, against
                 the chapters each problem is filed under - "same idea,
                 different problem" when nothing above fires.

They combine into one 0-100 score with the reasons listed, because the reasons
are what you will judge the edge cases by. The index is built lazily from the
bank and rebuilt when the bank changes.
"""

from __future__ import annotations

import json
import math
import os
import re
import threading

HERE = os.path.dirname(os.path.abspath(__file__))

try:
    from fpdb import html_to_text
except Exception:                                   # pragma: no cover
    def html_to_text(s: str) -> str:
        return re.sub(r"<[^>]+>", " ", s or "")

# words that carry no identity: function words plus the boilerplate every
# statement shares ("given", "return", "example", "input", "output" ...)
FUNCTION = set("""
a an the and or but if then else of to in on at by for from with without into
onto over under up down out as is are was were be been being have has had do
does did can could may might must shall should will would not no nor only
this that these those it its itself they them their there here where when
which who whom whose what why how all any both each few more most other some
such than too very same so also just yet even still ever never once again
you your yours we our ours he she his her him i me my mine
""".split())

STOP = set("""
a an the and or but if then else of to in on at by for from with without into
onto over under up down out as is are was were be been being have has had do
does did can could may might must shall should will would not no nor only
this that these those it its itself they them their there here where when
which who whom whose what why how all any both each few more most other some
such than too very same so also just yet even still ever never once again
you your yours we our ours he she his her him i me my mine one two three
given return returns returning find finds determine compute calculate count
output input example examples explanation note notes constraints constraint
problem statement function write implement implementation task tasks task's
let assume assuming consider following follows above below between every
each per within exactly least most minimum maximum possible impossible
valid invalid integer integers number numbers array arrays list lists string
strings value values element elements index indices size length n m k ith
first last second next previous new old true false none null
""".split())

# a story word is one that names the company's world, not the problem: the
# bank's company names are stripped automatically; these are the generic
# dressings statements use to look different
STORY = set("""
company companies team teams engineer engineers developer developers system
systems service services platform platforms customer customers user users
client clients product products order orders store stores shop warehouse
inventory package packages delivery deliveries driver drivers employee
employees manager managers office project projects department server servers
network networks data database log logs record records report reports
account accounts bank banking transaction transactions payment payments
""".split())

WORD = re.compile(r"[a-z][a-z0-9_']*|\d+(?:\.\d+)?")
CAMEL = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")
POWER = re.compile(r"(?:10\s*(?:\^|\*\*)\s*(\d+)|\b1e(\d+)\b|\b(10{3,})\b)")
LITERAL = re.compile(r"\"[^\"\n]{1,200}\"|'[^'\n]{1,200}'")
NUMBER = re.compile(r"-?\d+(?:\.\d+)?")
# a value announced as the answer counts however short it is: "Output: 3"
ANSWER = re.compile(r"(?i)(?:output|answer|result|returns?|expected|->|=>|⇒)\s*[:=]?\s*"
                    r"(-?\d+(?:\.\d+)?|true|false|null|none|\"[^\"\n]*\"|'[^'\n]*')")


# ------------------------------------------------------------- normalising
def words(text: str) -> list[str]:
    return WORD.findall((text or "").lower())


def stem(w: str) -> str:
    """Just enough to make tasks/task and ordering/order meet; nothing cleverer,
    because a wrong stem merges words that should stay apart."""
    if len(w) <= 3 or w.isdigit():
        return w
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith("sses"):
        return w[:-2]
    if w.endswith("s") and not w.endswith("ss") and not w.endswith("us"):
        w = w[:-1]
    if w.endswith("ing") and len(w) > 6:
        w = w[:-3]
    elif w.endswith("ed") and len(w) > 5:
        w = w[:-2]
    return w


def split_ident(name: str) -> list[str]:
    """countTarget -> [count, target]; max_profit -> [max, profit]."""
    out = []
    for part in re.split(r"[_\W]+", name or ""):
        out.extend(p.lower() for p in CAMEL.findall(part))
    return out


def magnitudes(text: str) -> set[str]:
    """10^5, 1e5 and 100000 all become 'e5'."""
    out = set()
    for a, b, c in POWER.findall(text or ""):
        if a:
            out.add("e" + a)
        elif b:
            out.add("e" + b)
        elif c:
            out.add("e%d" % (len(c) - 1))
    return out


def brackets(text: str) -> list[str]:
    """Every balanced [...] or {...} literal in the text, nesting allowed."""
    out = []
    stack = []
    start = -1
    pairs = {"[": "]", "{": "}"}
    for i, ch in enumerate(text or ""):
        if ch in pairs:
            if not stack:
                start = i
            stack.append(pairs[ch])
        elif stack and ch == stack[-1]:
            stack.pop()
            if not stack:
                out.append(text[start:i + 1])
        elif stack and ch in "]}" and ch != stack[-1]:
            stack = []                              # malformed: give up on it
    return out


def norm_literal(v: str) -> str:
    """So that [1, 2, 3] and [1,2,3] and "[1,2,3]" are the same literal."""
    s = (v or "").strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        s = s[1:-1]
    s = re.sub(r"\s+", "", s)
    s = s.replace("'", '"')
    return s.lower()


def literals(text: str) -> set[str]:
    """Example-like values in free text: bracketed structures, quoted strings,
    and bare numbers of at least two digits that are not constraint bounds."""
    out = set()
    for b in brackets(text):
        n = norm_literal(b)
        if len(n) >= 4:
            out.add(n)
    for q in LITERAL.findall(text or ""):
        n = norm_literal(q)
        if len(n) >= 3:
            out.add(n)
    stripped = POWER.sub(" ", text or "")
    for n in NUMBER.findall(stripped):
        if len(n.lstrip("-")) >= 2 and not re.fullmatch(r"-?10+", n):
            out.add(n)
    for a in ANSWER.findall(text or ""):
        out.add(norm_literal(a))
    return out


def distinct(lit: str) -> float:
    """How much a shared literal proves: a long array proves a lot, a two-digit
    number almost nothing."""
    if lit.startswith("[") or lit.startswith("{"):
        return min(1.0, 0.3 + len(lit) / 24.0)
    if re.fullmatch(r"-?\d+(?:\.\d+)?", lit):
        return 0.08 if len(lit) <= 3 else 0.2
    return min(0.8, 0.2 + len(lit) / 20.0)


# --------------------------------------------------------------- the index
class Index:
    def __init__(self, bank, topic_index: dict | None = None, companies=None):
        self.docs: dict[str, dict] = {}
        self.postings: dict[str, list[tuple[str, float]]] = {}
        self.idf: dict[str, float] = {}
        self.pairs: dict[tuple[str, str], set[str]] = {}       # (input literal, output) -> ids
        self.by_literal: dict[str, set[str]] = {}
        self.by_func: dict[str, set[str]] = {}
        self.story = set(STOP) | set(STORY)
        for c in companies or []:
            self.story.update(words(c))
        by_problem = (topic_index or {}).get("byProblem", {})
        self._build(bank, by_problem)

    # -- building
    def _build(self, bank, by_problem):
        tf_docs = {}
        df: dict[str, int] = {}
        for r in bank.conn.execute("SELECT id, title, detail_json FROM problems"):
            d = json.loads(r["detail_json"] or "{}")
            pid = r["id"]
            title = r["title"] or d.get("title") or pid
            statement = html_to_text(d.get("problemStatement") or "")
            cons = html_to_text(d.get("constraints") or "")
            text = " ".join([title, statement, cons])
            toks = self.tokens(text, title)
            tf: dict[str, int] = {}
            for t in toks:
                tf[t] = tf.get(t, 0) + 1
            for t in tf:
                df[t] = df.get(t, 0) + 1
            tf_docs[pid] = tf
            lits, pairs = set(), set()
            for ex in d.get("examples") or []:
                ins = [norm_literal(i.get("inputValue") or "") for i in (ex.get("inputText") or [])]
                out = norm_literal(ex.get("outputText") or "")
                for v in ins + [out]:
                    if len(v) >= 2:
                        lits.add(v)
                for v in ins:
                    if len(v) >= 2 and len(out) >= 1:
                        pairs.add((v, out))
            func = d.get("functionName") or ""
            params = []
            for ex in (d.get("examples") or [])[:1]:
                params = [i.get("inputName") or "" for i in (ex.get("inputText") or [])]
            self.docs[pid] = {
                "id": pid, "title": title, "company": d.get("company"),
                "family": " ".join(stem(w) for w in words(title) if w not in STOP),
                "titlewords": {stem(w) for w in words(title) if w not in FUNCTION and len(w) > 2},
                "difficulty": d.get("difficulty"),
                "func": " ".join(split_ident(func)), "params": set(split_ident(" ".join(params))),
                "mags": magnitudes(cons + " " + statement),
                "topics": set(by_problem.get(pid) or []),
                "literals": lits, "pairs": pairs,
            }
            for v in lits:
                self.by_literal.setdefault(v, set()).add(pid)
            for pr in pairs:
                self.pairs.setdefault(pr, set()).add(pid)
            if func:
                self.by_func.setdefault(" ".join(split_ident(func)), set()).add(pid)
        n = max(1, len(tf_docs))
        self.idf = {t: math.log((n + 1) / (c + 1)) + 1 for t, c in df.items()}
        for pid, tf in tf_docs.items():
            vec = {t: (1 + math.log(c)) * self.idf[t] for t, c in tf.items()}
            norm = math.sqrt(sum(w * w for w in vec.values())) or 1.0
            for t, w in vec.items():
                self.postings.setdefault(t, []).append((pid, w / norm))

    def tokens(self, text: str, title: str = "") -> list[str]:
        out = []
        for w in words(text):
            if w in self.story or len(w) < 2:
                continue
            if w.isdigit():
                continue                            # magnitudes are a signal of their own
            out.append(stem(w))
        # the title's words count twice: they are the author's own summary
        for w in words(title):
            if w not in self.story and len(w) >= 2 and not w.isdigit():
                out.append(stem(w))
        return out

    # -- querying
    def query_vector(self, text: str) -> dict[str, float]:
        tf: dict[str, int] = {}
        for t in self.tokens(text):
            if t in self.idf:
                tf[t] = tf.get(t, 0) + 1
        vec = {t: (1 + math.log(c)) * self.idf[t] for t, c in tf.items()}
        norm = math.sqrt(sum(w * w for w in vec.values())) or 1.0
        return {t: w / norm for t, w in vec.items()}

    def cosine_all(self, qv: dict[str, float]) -> dict[str, float]:
        acc: dict[str, float] = {}
        for t, qw in qv.items():
            for pid, dw in self.postings.get(t, ()):
                acc[pid] = acc.get(pid, 0.0) + qw * dw
        return acc


# ------------------------------------------------------------ the matcher
WEIGHTS = {"wording": 50, "examples": 30, "title": 10, "signature": 8, "constraints": 4,
           "concept": 8}


class Matcher:
    def __init__(self, bank, topics_mod=None):
        self.bank = bank
        self.topics_mod = topics_mod
        self._index: Index | None = None
        self._stamp = None
        self._lock = threading.Lock()
        self._canon = None

    def index(self) -> Index:
        stamp = self._bank_stamp()
        with self._lock:
            if self._index is None or stamp != self._stamp:
                companies = [r[0] for r in self.bank.conn.execute(
                    "SELECT DISTINCT json_extract(detail_json, '$.company') FROM problems") if r[0]]
                tidx = self.topics_mod.index() if self.topics_mod else None
                self._index = Index(self.bank, tidx, companies)
                self._stamp = stamp
        return self._index

    def _bank_stamp(self):
        try:
            return (os.path.getmtime(self.bank.path),
                    self.bank.conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0])
        except Exception:
            return None

    def concept(self, text: str) -> list[str]:
        """The chapters this text would be filed under, by the canon's own scorer."""
        try:
            if self._canon is None:
                import sys
                sys.path.insert(0, os.path.join(HERE, "tools"))
                import topicmap
                self._canon = (topicmap, topicmap.compiled())
            topicmap, canon = self._canon
        except Exception:
            return []
        hits = []
        for t in canon:
            s, _ = topicmap.score(t, set(), "", text)
            if s:
                hits.append((s, t["slug"]))
        hits.sort(key=lambda h: (-h[0], h[1]))
        return [slug for _, slug in hits[:6]]

    def find(self, text: str, limit: int = 10) -> dict:
        idx = self.index()
        text = text or ""
        qv = idx.query_vector(text)
        cos = idx.cosine_all(qv)
        q_lits = literals(text)
        q_mags = magnitudes(text)
        q_topics = set(self.concept(text)) if len(text) > 40 else set()
        func_words = set()
        m = re.search(r"\b(?:def|function|public\s+\w+|int|string|bool)\s+([A-Za-z_]\w*)\s*\(", text)
        if m:
            func_words = set(split_ident(m.group(1)))
        q_words = set(words(text))
        q_stems = {stem(w) for w in q_words}

        # candidates: anything with wording in common, plus anything sharing a
        # literal or a function name - a pasted example with no prose must
        # still find its problem
        cands = set(cos)
        for v in q_lits:
            cands |= idx.by_literal.get(v, set())
        if func_words:
            cands |= idx.by_func.get(" ".join(sorted(func_words)), set())

        # a short paraphrase can never reach the cosine a full paste does, so
        # wording is judged half against an absolute bar and half against the
        # best candidate there is
        top = max(cos.values()) if cos else 0.0
        scored = []
        for pid in cands:
            d = idx.docs[pid]
            why = []
            parts = {}

            c = cos.get(pid, 0.0)
            rel = c / top if top > 0 else 0.0
            parts["wording"] = 0.5 * min(1.0, c / 0.6) + 0.5 * (rel if c >= 0.12 else 0.0)
            if c >= 0.5:
                why.append("wording: very close (%.2f)" % c)
            elif c >= 0.25:
                why.append("wording: close (%.2f)" % c)
            elif c >= 0.12 and rel >= 0.8:
                why.append("wording: the closest there is (%.2f)" % c)

            shared = q_lits & d["literals"]
            pair_hits = [p for p in d["pairs"] if p[0] in q_lits and p[1] in q_lits]
            ex = 0.0
            if pair_hits:
                ex = 1.0
                why.append("example: same input and output (%s -> %s)"
                           % (_short(pair_hits[0][0]), _short(pair_hits[0][1])))
            elif shared:
                ex = min(0.7, sum(distinct(v) for v in shared))
                best = max(shared, key=distinct)
                if distinct(best) >= 0.3:
                    why.append("example: shares the value %s" % _short(best))
            parts["examples"] = ex

            # the title is the author's own summary; a paraphrase that repeats
            # most of it is talking about the same thing
            tw = d["titlewords"]
            tt = len(tw & q_stems) / len(tw) if tw else 0.0
            parts["title"] = tt if tt >= 0.5 else 0.0
            if tt >= 0.67 and len(tw) >= 2:
                why.append("title words in the text: " + ", ".join(sorted(tw & q_stems)[:4]))

            sig = 0.0
            fw = set(d["func"].split())
            if fw and func_words and fw == func_words:
                sig = 1.0
                why.append("same function name")
            elif fw and fw <= q_words and len(fw) >= 2:
                sig = 0.6
                why.append("function name appears in the text")
            shared_params = {w for w in d["params"] & q_words if w not in STOP and len(w) > 2}
            if len(shared_params) >= 2 and len(shared_params) >= len(d["params"]) // 2:
                sig = max(sig, 0.5)
                if sig == 0.5:
                    why.append("same parameter names: " + ", ".join(sorted(shared_params)[:3]))
            parts["signature"] = sig

            mg = 0.0
            if q_mags and d["mags"]:
                mg = len(q_mags & d["mags"]) / len(q_mags | d["mags"])
                if mg >= 0.5:
                    why.append("same constraints (" + ", ".join(sorted(q_mags & d["mags"])) + ")")
            parts["constraints"] = mg

            cp = 0.0
            if q_topics and d["topics"]:
                cp = len(q_topics & d["topics"]) / len(q_topics | d["topics"])
                if cp >= 0.34:
                    cp_names = sorted(q_topics & d["topics"])
                    why.append("same chapters: " + ", ".join(cp_names[:3]))
            parts["concept"] = cp

            total = sum(WEIGHTS[k] * v for k, v in parts.items())
            # a shared example pair is near-proof even when the story is new
            if pair_hits and total < 75:
                total = 75 + (total - 75) * 0.2 + 10 * parts["wording"]
            total = max(0.0, min(100.0, total))
            scored.append((total, pid, parts, why))

        scored.sort(key=lambda s: (-s[0], s[1]))
        # the bank holds the same problem under several companies; one row per
        # family, the best-scoring copy first and the others named on it
        results, seen = [], {}
        for total, pid, parts, why in scored:
            d = idx.docs[pid]
            key = d["family"]
            if key in seen:
                seen[key]["also"].append({"id": pid, "company": d["company"], "score": round(total)})
                continue
            if len(results) >= limit:
                continue
            row = {
                "id": pid, "title": d["title"], "company": d["company"],
                "difficulty": d["difficulty"], "score": round(total),
                "label": label(total, parts), "why": why,
                "parts": {k: round(v, 2) for k, v in parts.items()},
                "also": [],
            }
            results.append(row)
            seen.setdefault(key, row)
        return {
            "results": results,
            "query": {"terms": len(qv), "literals": len(q_lits),
                      "magnitudes": sorted(q_mags), "topics": sorted(q_topics),
                      "candidates": len(cands)},
        }


def label(total: float, parts: dict) -> str:
    """What the evidence supports, not what the number says: a one-line
    paraphrase can never score like a full paste, but can still be certain."""
    ex, w, t = parts.get("examples", 0), parts.get("wording", 0), parts.get("title", 0)
    corroborated = sum(1 for k in ("title", "signature", "constraints") if parts.get(k, 0) >= 0.5)
    sig = parts.get("signature", 0)
    if ex >= 1.0 or total >= 75 or (w >= 0.8 and (t >= 0.5 or sig >= 1.0 or corroborated >= 2)):
        return "same problem"
    if total >= 50 or (w >= 0.7 and (t >= 0.5 or ex >= 0.3)):
        return "probably the same"
    if total >= 35 or parts.get("concept", 0) >= 0.34:
        return "related"
    return "weak"


def _short(v: str, n: int = 28) -> str:
    return v if len(v) <= n else v[:n - 1] + "…"

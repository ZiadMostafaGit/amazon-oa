# Inverted index from token to query ids, matching a log by counting covered query tokens.
from typing import Dict, List


def _tokens(payload: str) -> set:
    out = set()
    cur = []
    for ch in payload:
        if ch.isascii() and ch.isalnum():
            cur.append(ch.lower())
        elif cur:
            out.add("".join(cur))
            cur = []
    if cur:
        out.add("".join(cur))
    return out


def processLiveTail(stream: List[str]) -> List[str]:
    res: List[str] = []
    index: Dict[str, List[int]] = {}
    sizes: List[int] = []  # sizes[id-1] = number of distinct tokens in that query
    next_id = 0
    for event in stream:
        kind = event[0]
        payload = event[3:] if len(event) > 3 else ""
        toks = _tokens(payload)
        if kind == 'Q':
            next_id += 1
            sizes.append(len(toks))
            for t in toks:
                index.setdefault(t, []).append(next_id)
            res.append("ACK: %s; ID=%d" % (payload, next_id))
        else:
            hits: Dict[int, int] = {}
            for t in toks:
                for qid in index.get(t, ()):  # type: ignore[arg-type]
                    hits[qid] = hits.get(qid, 0) + 1
            matched = sorted(qid for qid, c in hits.items() if c == sizes[qid - 1])
            if matched:
                res.append("M: %s; Q=%s" % (payload, ",".join(map(str, matched))))
    return res

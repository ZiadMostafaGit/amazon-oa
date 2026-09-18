# Dict of last vote per (user, article) plus an ordered recency list of flipped articles per user.
from typing import List, Optional, Any


def processArticleVotes(operations: List[List[str]]) -> List[List[str]]:
    titles = {}          # article id (str) -> title
    next_id = 1
    last_vote = {}       # (user, article id) -> "UPVOTE" / "DOWNVOTE"
    flips = {}           # user -> list of article ids, most recent last
    out = []

    for op in operations:
        kind = op[0]
        if kind == "ADD":
            aid = str(next_id)
            next_id += 1
            titles[aid] = op[1]
            out.append([aid])
        elif kind in ("UPVOTE", "DOWNVOTE"):
            aid = op[1]
            user = op[2]
            key = (user, aid)
            prev = last_vote.get(key)
            last_vote[key] = kind
            if prev is not None and prev != kind:
                lst = flips.setdefault(user, [])
                if aid in lst:
                    lst.remove(aid)
                lst.append(aid)
        elif kind == "LAST_THREE":
            user = op[1]
            lst = flips.get(user, [])
            recent = lst[-3:][::-1]
            out.append([titles[a] for a in recent])
    return out

# Deduplicate records, build hash indexes per policy/post/time, and bisect a sorted time axis for range queries.
from typing import List, Optional, Any
from bisect import bisect_left, bisect_right


def answerViolationQueries(records: List[List[str]], queries: List[List[str]]) -> List[str]:
    unique = set()
    for rec in records:
        unique.add((rec[0], rec[1], int(rec[2])))

    posts_by_policy = {}
    policies_by_post = {}
    posts_at_time = {}
    by_time = {}
    for post, policy, ts in unique:
        posts_by_policy.setdefault(policy, set()).add(post)
        policies_by_post.setdefault(post, set()).add(policy)
        posts_at_time.setdefault(ts, set()).add(post)
        by_time.setdefault(ts, []).append((post, policy))

    times = sorted(by_time)
    buckets = [by_time[t] for t in times]

    range_posts_cache = {}
    range_counts_cache = {}

    def bounds(start: int, end: int):
        if start > end:
            return 0, 0
        return bisect_left(times, start), bisect_right(times, end)

    out: List[str] = []
    for q in queries:
        kind = q[0]
        if kind == "POSTS_BY_POLICY":
            out.append(",".join(sorted(posts_by_policy.get(q[1], ()))))
        elif kind == "POLICIES_BY_POST":
            out.append(",".join(sorted(policies_by_post.get(q[1], ()))))
        elif kind == "POSTS_AT_TIME":
            out.append(",".join(sorted(posts_at_time.get(int(q[1]), ()))))
        elif kind == "POSTS_IN_RANGE":
            start, end = int(q[1]), int(q[2])
            key = (start, end)
            cached = range_posts_cache.get(key)
            if cached is None:
                lo, hi = bounds(start, end)
                found = set()
                for i in range(lo, hi):
                    for post, _policy in buckets[i]:
                        found.add(post)
                cached = ",".join(sorted(found))
                range_posts_cache[key] = cached
            out.append(cached)
        elif kind == "COUNTS_BY_POLICY":
            start, end = int(q[1]), int(q[2])
            key = (start, end)
            cached = range_counts_cache.get(key)
            if cached is None:
                lo, hi = bounds(start, end)
                counts = {}
                for i in range(lo, hi):
                    for _post, policy in buckets[i]:
                        counts[policy] = counts.get(policy, 0) + 1
                cached = ",".join(
                    "%s=%d" % (p, counts[p]) for p in sorted(counts)
                )
                range_counts_cache[key] = cached
            out.append(cached)
        else:
            out.append("")
    return out

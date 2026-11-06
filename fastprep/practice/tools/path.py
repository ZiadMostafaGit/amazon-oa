#!/usr/bin/env python3
"""Build the DSA learning path: topics in the order to learn them, problems in the order to solve them.

    python3 tools/path.py            # rebuild path/PATH.json and fixes/khatt.json
    python3 tools/path.py --dry      # print the path, write nothing

THE ORDER
  Phase A, OA core. What online assessments actually test, measured on this bank's OA
  problems: greedy, sorting, hashing, simulation, prefix sums, binary search, heaps. These come
  first because they pay off first; each also needs nothing that comes after it.
  Phase B, interview core. Trees, graphs, DP, backtracking: rarer in OAs (about 1% each of
  recent Amazon OA problems) but the backbone of phone screens and onsites.
  Phase C, depth. The rest, once the core is automatic.

THE ORDER INSIDE A STAGE
  1. the chapter (in the study space)
  2. one or two CLASSIC forms of the pattern, the clean textbook version, to learn it on
  3. OA forms - the same pattern wrapped in a story, as companies ask it - easy, then medium, then hard
  4. "more practice": the next problems on the same pattern, for when the week's set is done
  Re-solves are scheduled by the study space (3, 10, 30, 90 days) once a problem is marked solved.

Each stage is tied to a week of the KHATT plan. Weeks the path does not own (practice sets:
company weeks, gauntlets, mixed OA sims) keep the problems already scheduled there.
"""
import collections, difflib, json, math, os, re, sqlite3, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(os.path.dirname(HERE), "fastprep.db")
OUT = os.path.join(HERE, "path", "PATH.json")
KHATT = os.path.join(HERE, "fixes", "khatt.json")
MORE = 20
DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu"]

# (slug, title, KHATT week, chapters, bank tags (any), classic titles)
PHASES = [
    ("OA core", "What online assessments test most. Learn these first: they pay off first.", [
        ("arrays-hashing", "Arrays & Hashing", 1, ["arrays", "hash-tables", "frequency-counting", "anagrams"],
         {"hash_table"}, ["Two Sum", "Contains Duplicate", "Valid Anagram", "Group Anagrams", "Top K Frequent Elements"]),
        ("sorting-two-pointers", "Sorting & Two Pointers", 2, ["sorting", "custom-comparators", "two-pointers"],
         {"sorting", "two_pointers"}, ["3Sum", "Container With Most Water", "Sort Colors", "Valid Palindrome",
                                       "Two Sum II", "Merge Sorted Array", "Squares of a Sorted Array"]),
        ("greedy", "Greedy I: sort, then choose", 3, ["greedy"],
         {"greedy"}, ["Assign Cookies", "Jump Game", "Gas Station", "Boats to Save People", "Lemonade Change"]),
        ("prefix-window", "Prefix Sums & Sliding Window", 4, ["prefix-sums", "sliding-window"],
         {"prefix_sum", "sliding_window"}, ["Subarray Sum Equals K", "Range Sum Query", "Product of Array Except Self",
                                            "Longest Substring Without Repeating Characters", "Minimum Size Subarray Sum"]),
        ("simulation", "Simulation & Strings: careful implementation", 5, ["simulation", "strings", "parsing", "matrix-traversal"],
         {"simulation"}, ["Spiral Matrix", "Game of Life", "Rotate Image", "String Compression", "Robot Return to Origin"]),
        ("binary-search", "Binary Search, and on the answer", 6, ["binary-search", "binary-search-on-answer", "search-rotated"],
         {"binary_search"}, ["Binary Search", "Koko Eating Bananas", "Search Insert Position",
                             "Capacity To Ship Packages Within D Days", "Find Minimum in Rotated Sorted Array"]),
        ("heap", "Heaps & Priority Queues", 7, ["heap", "top-k", "k-way-merge", "median-maintenance"],
         {"heap"}, ["Kth Largest Element in an Array", "Last Stone Weight", "K Closest Points to Origin",
                    "Task Scheduler", "Merge k Sorted Lists", "Find Median from Data Stream"]),
        ("greedy-intervals", "Greedy II: exchange arguments & intervals", 8,
         ["greedy-exchange", "intervals", "scheduling", "sweep-line"],
         {"intervals", "greedy"}, ["Merge Intervals", "Non-overlapping Intervals", "Meeting Rooms II", "Insert Interval",
                                   "Minimum Number of Arrows to Burst Balloons"]),
        ("stack", "Stacks & Monotonic Stacks", 9, ["stack", "monotonic-stack"],
         {"stack"}, ["Valid Parentheses", "Min Stack", "Daily Temperatures", "Next Greater Element",
                     "Evaluate Reverse Polish Notation", "Largest Rectangle in Histogram"]),
    ]),
    ("Interview core", "Rarer in OAs, but the backbone of phone screens and onsites.", [
        ("lists-trees", "Linked Lists & Trees: DFS and BFS", 10, ["linked-list", "trees", "tree-traversal", "dfs", "bfs"],
         {"linked_list", "tree"}, ["Reverse Linked List", "Merge Two Sorted Lists", "Linked List Cycle",
                                   "Maximum Depth of Binary Tree", "Invert Binary Tree", "Binary Tree Level Order Traversal"]),
        ("trees-2", "Trees II: BST, LCA, tries", 11, ["bst", "lca", "trie", "serialize-tree"],
         {"tree", "trie"}, ["Validate Binary Search Tree", "Lowest Common Ancestor", "Kth Smallest Element in a BST",
                            "Implement Trie", "Serialize and Deserialize Binary Tree"]),
        ("graphs", "Graphs: BFS/DFS, grids, topological sort", 12,
         ["graphs", "bfs", "dfs", "topological-sort", "flood-fill", "grid-bfs", "multi-source-bfs"],
         {"graph", "breadth_first_search", "depth_first_search", "topological_sort"},
         ["Number of Islands", "Course Schedule", "Rotting Oranges", "Clone Graph", "Flood Fill"]),
        ("graphs-2", "Graphs II: union-find & shortest paths", 14, ["union-find", "shortest-path", "dijkstra"],
         {"union_find", "shortest_path"}, ["Number of Provinces", "Redundant Connection", "Network Delay Time",
                                           "Path With Minimum Effort", "Cheapest Flights Within K Stops"]),
        ("dp-1", "Dynamic Programming I: 1-D", 15, ["dynamic-programming", "dp-1d", "memoization"],
         {"dynamic_programming"}, ["Climbing Stairs", "House Robber", "Coin Change", "Decode Ways", "Word Break",
                                   "Min Cost Climbing Stairs"]),
        ("dp-1b", "Dynamic Programming I: LIS, Kadane, counting", 16, ["lis", "kadane", "counting-dp", "dynamic-programming"],
         {"dynamic_programming"}, ["Longest Increasing Subsequence", "Maximum Subarray", "Maximum Product Subarray",
                                   "Unique Paths", "Partition Equal Subset Sum"]),
        ("backtracking", "Backtracking", 17, ["backtracking", "subsets", "permutations"],
         {"backtracking"}, ["Subsets", "Permutations", "Combination Sum", "Generate Parentheses", "Word Search"]),
    ]),
    ("Depth", "The rest, once the core is automatic.", [
        ("dp-2", "Dynamic Programming II: knapsack, grids, strings", 20, ["knapsack", "unbounded-knapsack", "dp-strings", "dp-2d"],
         {"dynamic_programming"}, None),
        ("bits-math", "Bits & Maths", 21, ["bit-manipulation", "xor-tricks", "math", "number-theory", "geometry"],
         {"bit_manipulation", "math"}, None),
        ("adv-graphs", "Advanced Graphs", 23, ["shortest-path", "bridges-articulation", "minimum-spanning-tree"],
         {"shortest_path", "graph"}, None),
        ("range-queries", "Range Queries: segment tree & Fenwick", 27, ["segment-tree", "fenwick-tree", "sqrt-decomposition"],
         {"segment_tree"}, None),
        ("dp-3", "Interval, game and bitmask DP", 28, ["partition-dp", "game-dp", "tree-dp", "dp-bitmask"],
         {"dynamic_programming"}, None),
        ("string-algos", "String algorithms: KMP, Z, hashing", 35, ["string-matching", "palindromes", "manachers"],
         {"string"}, None),
        ("design-coding", "Design-style coding: LRU, iterators, rate limiters", 38,
         ["design-data-structure", "lru-cache", "rate-limiting"], {"design"}, None),
    ]),
]
# weeks whose plan problems are kept as scheduled (W1 is already under way; Phase C weeks were
# picked per pattern already); every other week the path owns is re-picked
KEEP_WEEKS = {1, 20, 21, 23, 27, 28, 35, 38}
BAD_TOPIC = {"concurrency", "database"}
BAD_TITLE = re.compile(r"scratch|classifier|neural|regression|gradient|transformer|tokeni[sz]|goroutine|thread|mutex|\bsql\b|pandas|llm", re.I)
DIFF = {"easy": 0, "medium": 1, "hard": 2}
# problems whose published examples contradict their own source: never scheduled
EXCLUDE = {"amazon-count-special-substrs", "amazon-find-first-index-where-prefix-sum-becomes-non-positive",
           "uber-counting-segments-after-house-removals", "tiktok-get-server-index"}


def norm(t):
    t = re.sub(r"\(.*?\)", " ", (t or "").lower())
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def load():
    c = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
    verified = set()
    try:
        verified = {k for k, v in json.load(open(os.path.join(HERE, "solutions", "VERIFIED.json")))["problems"].items() if v.get("ok")}
    except (OSError, ValueError):
        pass
    fixed = {f[:-5] for f in os.listdir(os.path.join(HERE, "fixes")) if f.endswith(".json") and f != "khatt.json"}
    P = {}
    for pid, d in c.execute("SELECT id, detail_json FROM problems"):
        d = json.loads(d or "{}")
        if d.get("practiceFormat", "algorithm") != "algorithm":
            continue
        st = re.sub(r"<[^>]+>", "", d.get("problemStatement") or "")
        P[pid] = dict(id=pid, title=d.get("title") or pid, company=d.get("company") or "",
                      diff=(d.get("difficulty") or "medium").lower(), stages=d.get("problemTypes") or [],
                      last=max(d.get("lastSeen") or [""]), seen=d.get("seenCount") or 1, stlen=len(st),
                      imgs=len(d.get("sourceImages") or []), ex=len(d.get("examples") or []),
                      tags=set(d.get("topics") or []), verified=pid in verified, fixed=pid in fixed)
    index = json.load(open(os.path.join(HERE, "topics", "INDEX.json")))
    chap = {t["slug"]: set(t.get("problems") or []) for t in index["topics"]}
    titles = {t["slug"]: t["title"] for t in index["topics"]}
    return P, chap, titles


def quality(p):
    if p["stlen"] < 200 and not p["imgs"] and not p["fixed"]:
        return None
    if p["id"] in EXCLUDE or BAD_TOPIC & p["tags"] or BAD_TITLE.search(p["title"]):
        return None
    q = 4 if p["fixed"] else 0
    q += 3 if p["verified"] else 0
    q += 2 if "OA" in p["stages"] else 0
    q += 1.5 if p["company"] == "Amazon" else 0
    q += 1 if p["last"] >= "2025-06-01" else 0
    q += min(2, math.log2(p["seen"]))
    q += 1 if p["ex"] >= 2 else 0
    q += 1 if p["stlen"] >= 400 or p["imgs"] else 0
    return q


def curve(n):
    """How many classic / easy / medium / hard problems a stage of n gets."""
    classic = 2 if n >= 8 else 1
    hard = 1 if n >= 9 else 0
    easy = max(1, round(0.2 * n))
    return classic, easy, n - classic - easy - hard, hard


def main(argv):
    dry = "--dry" in argv
    P, chap, ctitle = load()
    khatt = json.load(open(KHATT))
    slots = collections.defaultdict(list)          # week -> [day, ...] in order
    for pid, v in khatt.items():
        slots[v["week"]].append(v["day"])
    order = {d: i for i, d in enumerate(DAYS + ["optional"])}
    for w in slots:
        slots[w].sort(key=lambda d: order.get(d, 9))
    path_weeks = {s[2] for _, _, st in PHASES for s in st}
    kept = {pid: v for pid, v in khatt.items() if v["week"] not in path_weeks or v["week"] in KEEP_WEEKS}
    used = set(kept)
    used_titles = {norm(P[p]["title"]) for p in kept if p in P}

    def take(pid):
        used.add(pid)
        used_titles.add(norm(P[pid]["title"]))

    def free(p):
        return p["id"] not in used and norm(p["title"]) not in used_titles

    phases_out, new_khatt = [], dict(kept)
    for ptitle, pabout, stages in PHASES:
        st_out = []
        for slug, title, week, chapters, tags, classics in stages:
            pool_ids = set().union(*(chap.get(c, set()) for c in chapters))
            def cands(require_tag=True):
                for pid, p in P.items():
                    if not free(p):
                        continue
                    if require_tag and not (tags & p["tags"]):
                        continue
                    q = quality(p)
                    if q is None:
                        continue
                    yield p, q + (2 if pid in pool_ids else 0)
            n = len(slots.get(week, [])) or 8
            plan = []
            n_classic = 0
            if week in KEEP_WEEKS:
                plan = sorted((pid for pid, v in kept.items() if v["week"] == week),
                              key=lambda pid: (order.get(kept[pid]["day"], 9), DIFF.get(P.get(pid, {}).get("diff"), 1)))
                for pid in plan:
                    take(pid)
            else:
                c_n, e_n, m_n, h_n = curve(n)
                # 1. classics: the bank's own copies of the textbook problems
                for ct in classics or []:
                    if len(plan) >= c_n:
                        break
                    best = None
                    for p, q in cands(require_tag=False):
                        r = difflib.SequenceMatcher(None, norm(ct), norm(p["title"])).ratio()
                        if r >= 0.86 and p["diff"] != "hard" and (best is None or (r, q) > best[0]):
                            best = ((r, q), p["id"])
                    if best:
                        plan.append(best[1]); take(best[1])
                n_classic = len(plan)
                # 2. OA forms along the difficulty curve
                want = [("easy", e_n + (c_n - len(plan))), ("medium", m_n), ("hard", h_n)]
                for diff, k in want:
                    ranked = sorted(((q + (2 if "OA" in p["stages"] else 0), p["id"]) for p, q in cands() if p["diff"] == diff),
                                    reverse=True)
                    for _, pid in ranked[:k]:
                        plan.append(pid); take(pid)
                # fill if a difficulty ran dry
                while len(plan) < n:
                    ranked = sorted(((q, p["id"]) for p, q in cands()), reverse=True)
                    if not ranked:
                        break
                    plan.append(ranked[0][1]); take(ranked[0][1])
                for i, pid in enumerate(plan):
                    new_khatt[pid] = {"week": week, "day": slots[week][i] if i < len(slots[week]) else "optional",
                                      "label": title}
            # 3. more practice: the next best on the pattern, easy -> hard
            more = sorted(((q, p["id"]) for p, q in cands()), reverse=True)[:MORE]
            more_ids = [pid for _, pid in sorted(more, key=lambda t: (DIFF.get(P[t[1]]["diff"], 1), -t[0]))]
            for pid in more_ids:
                take(pid)
            st_out.append(dict(slug=slug, title=title, week=week,
                               chapters=[{"slug": c, "title": ctitle.get(c, c)} for c in chapters if c in ctitle],
                               tags=sorted(tags), plan=plan, classics=n_classic, more=more_ids))
        phases_out.append(dict(title=ptitle, about=pabout, stages=st_out))

    # how often each stage's tags appear in recent OA problems, so the order explains itself
    recent = [p for p in P.values() if "OA" in p["stages"] and p["last"] >= "2025-05-01"]
    amazon = [p for p in recent if p["company"] == "Amazon"]
    for ph in phases_out:
        for s in ph["stages"]:
            t = set(s["tags"])
            s["oaShare"] = round(100 * sum(1 for p in recent if t & p["tags"]) / max(1, len(recent)))
            s["amazonShare"] = round(100 * sum(1 for p in amazon if t & p["tags"]) / max(1, len(amazon)))

    # practice sets: the plan weeks the path does not own
    sets = collections.defaultdict(list)
    for pid, v in new_khatt.items():
        if v["week"] not in path_weeks:
            sets[v["week"]].append(pid)
    sets_out = [dict(week=w, ids=sorted(ids, key=lambda pid: order.get(new_khatt[pid]["day"], 9)),
                     label=collections.Counter(new_khatt[i]["label"] for i in ids).most_common(1)[0][0])
                for w, ids in sorted(sets.items())]

    out = dict(about=__doc__.split("THE ORDER")[0].strip().splitlines()[0], phases=phases_out, sets=sets_out,
               oaSample=len(recent), amazonSample=len(amazon))
    n_plan = sum(len(s["plan"]) for ph in phases_out for s in ph["stages"])
    n_more = sum(len(s["more"]) for ph in phases_out for s in ph["stages"])
    for ph in phases_out:
        print("==", ph["title"])
        for s in ph["stages"]:
            print("  W%02d %-48s plan %2d more %2d  OA %2d%% Amazon %2d%%  | %s"
                  % (s["week"], s["title"], len(s["plan"]), len(s["more"]), s["oaShare"], s["amazonShare"],
                     ", ".join(P[p]["title"][:28] for p in s["plan"][:3])))
    print("plan problems %d, more practice %d, KHATT %d" % (n_plan, n_more, len(new_khatt)))
    if dry:
        return 0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, "w"), indent=1)
    json.dump(dict(sorted(new_khatt.items(), key=lambda kv: (kv[1]["week"], order.get(kv[1]["day"], 9), kv[0]))),
              open(KHATT, "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""The roadmap: a tree of topics, each with the techniques it teaches and the problems that teach them.

    python3 tools/roadmap.py pools      # write roadmap/pools/<node>.txt: the candidates each node may curate from
    python3 tools/roadmap.py build      # assemble roadmap/ROADMAP.json from roadmap/nodes/*.json, rewrite fixes/khatt.json
    python3 tools/roadmap.py status     # which nodes are curated, how many problems, how many repaired

A NODE is a topic in the tree (like a NeetCode roadmap box). Its parents are the topics it needs. Its
`order` is the recommended order: prerequisites first, and among what is unlocked, what online
assessments ask most (greedy and sorting are 41% and 33% of recent Amazon OA problems; trees and graphs
about 1% each).

A node teaches a list of TECHNIQUES, the ideas you must own to say you know the topic. Curation (done by
reading the problems, not by tags) picks a LADDER: each technique introduced by the problem that teaches
it most clearly, then OA-style problems that mix them, then a stretch. roadmap/nodes/<node>.json:

    {"node": "knapsack", "ladder": [{"id": ..., "teaches": "<technique>", "why": "...", "level": "core|practice|stretch"}, ...]}

The first problems of a node's ladder are the ones the KHATT plan schedules in that node's week.
"""
import collections, json, math, os, re, sqlite3, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(os.path.dirname(HERE), "fastprep.db")
DIR = os.path.join(HERE, "roadmap")
KHATT = os.path.join(HERE, "fixes", "khatt.json")

# id, title, parents, phase, KHATT week(s), chapters (main first), bank tags, techniques
NODES = [
    ("arrays-hashing", "Arrays & Hashing", [], "A", [1], ["hash-tables", "arrays", "frequency-counting", "anagrams"], {"hash_table"}, [
        "a set to remember what you have seen", "a map from value to index (look up the complement)",
        "counting with a frequency map", "a canonical key to group things (sorted string, count signature)",
        "buckets indexed by frequency or value", "the array index as the hash (in-place marking)"]),
    ("sorting", "Sorting & Custom Order", ["arrays-hashing"], "A", [2], ["sorting", "custom-comparators"], {"sorting"}, [
        "sort, then compare neighbours", "sort by a key, a tuple or a custom comparator",
        "sort indices to keep original positions", "counting sort when values are small",
        "sort first so a greedy or two-pointer scan becomes valid"]),
    ("two-pointers", "Two Pointers", ["sorting"], "A", [2], ["two-pointers", "in-place-rearrangement"], {"two_pointers"}, [
        "converging pointers on a sorted array (pair sum)", "fix one element, two-pointer the rest, skip duplicates (3Sum)",
        "reader and writer pointers (compact in place)", "walk two sequences together (merge)",
        "move the side that cannot improve (container)", "compare from both ends (palindromes)"]),
    ("greedy", "Greedy", ["sorting"], "A", [3], ["greedy", "greedy-exchange"], {"greedy"}, [
        "sort, then take the locally best", "track the furthest reach so far",
        "a running balance that resets (gas station)", "pair the extremes",
        "prove the order with an exchange argument", "greedy with a counter or a heap of the best so far"]),
    ("prefix-sums", "Prefix Sums", ["arrays-hashing"], "A", [4], ["prefix-sums"], {"prefix_sum"}, [
        "range sum in O(1) from a prefix array", "prefix sum + hash map to count subarrays with sum k",
        "prefix of a parity, a mod or a balance", "difference array for range updates",
        "prefix and suffix arrays (product except self, best left and right)", "2-D prefix sums"]),
    ("sliding-window", "Sliding Window", ["two-pointers"], "A", [4], ["sliding-window"], {"sliding_window"}, [
        "fixed-size window", "variable window: the longest valid (shrink while invalid)",
        "variable window: the shortest valid (shrink while valid)", "window with a frequency map (distinct counts, anagrams)",
        "exactly k = at most k minus at most k-1", "window maximum with a monotonic deque"]),
    ("simulation", "Simulation & Implementation", ["arrays-hashing"], "A", [5], ["simulation", "matrix-traversal", "parsing", "strings"], {"simulation"}, [
        "step a state machine exactly as described", "walk a matrix with direction arrays (spiral, rotate)",
        "parse and tokenise a string", "process events in time order",
        "keep the bookkeeping straight: off-by-one, empty input, ties"]),
    ("binary-search", "Binary Search", ["sorting"], "A", [6], ["binary-search", "search-rotated"], {"binary_search"}, [
        "the first index where a monotone condition becomes true", "count elements <= x with bisect",
        "search a rotated sorted array", "search a sorted 2-D matrix"]),
    ("bs-answer", "Binary Search on the Answer", ["binary-search", "greedy"], "A", [6], ["binary-search-on-answer"], {"binary_search"}, [
        "minimise the maximum (capacity, speed)", "maximise the minimum (distance, gap)",
        "a greedy feasibility check inside the search", "binary search over real numbers or huge ranges"]),
    ("heap", "Heaps & Priority Queues", ["sorting"], "A", [7], ["heap", "top-k", "k-way-merge", "median-maintenance"], {"heap"}, [
        "top k with a heap of size k", "repeatedly take the best and push back the rest (simulate)",
        "merge k sorted lists", "two heaps for a running median", "a heap of events or end times (scheduling)"]),
    ("intervals", "Intervals", ["sorting", "greedy"], "A", [8], ["intervals", "sweep-line", "scheduling"], {"intervals"}, [
        "sort by start and merge overlaps", "insert an interval and test overlap",
        "the most non-overlapping intervals (sort by end)", "the fewest rooms: a sweep or a heap of end times",
        "a line sweep with +1 / -1 events"]),
    ("stack", "Stacks", ["arrays-hashing"], "A", [9], ["stack", "parsing"], {"stack"}, [
        "match pairs (parentheses)", "evaluate an expression (RPN, a calculator)",
        "simulate with undo or collapse (asteroids, removing pairs)", "a stack augmented with extra data (min stack)",
        "a stack of (value, count)"]),
    ("monotonic-stack", "Monotonic Stack", ["stack"], "A", [9], ["monotonic-stack"], {"stack"}, [
        "the next greater or smaller element", "a span or the distance to the next warmer day",
        "the largest rectangle in a histogram", "the contribution of each element (sum of subarray minimums)",
        "the lexicographically smallest result (remove k digits)"]),
    ("linked-list", "Linked Lists", ["two-pointers"], "B", [10], ["linked-list", "fast-slow-pointers", "lru-cache"], {"linked_list"}, [
        "reverse in place", "a dummy head to merge or delete", "fast and slow pointers (middle, cycle)",
        "a gap of k between two pointers (k-th from the end)", "a hash map plus a doubly linked list (LRU)"]),
    ("trees", "Trees: DFS & BFS", ["linked-list"], "B", [10], ["trees", "tree-traversal", "dfs", "bfs"], {"tree"}, [
        "recursive DFS that returns a value (depth, size)", "DFS that passes state down (path sums)",
        "level-order BFS", "post-order: combine the children's answers (diameter, balanced)",
        "build a tree from traversals"]),
    ("bst", "Binary Search Trees", ["trees", "binary-search"], "B", [11], ["bst", "lca", "balanced-bst"], {"tree"}, [
        "inorder traversal is sorted", "validate with lower and upper bounds",
        "search and insert by the ordering", "lowest common ancestor", "k-th smallest"]),
    ("trie", "Tries", ["trees"], "B", [11], ["trie"], {"trie"}, [
        "insert, search and starts-with", "count words with a prefix",
        "a trie plus DFS to search many words at once", "a bitwise trie for the maximum XOR"]),
    ("graphs", "Graphs: BFS & DFS", ["trees"], "B", [12], ["graphs", "bfs", "dfs", "flood-fill", "grid-bfs", "multi-source-bfs", "graph-modelling"],
     {"graph", "breadth_first_search", "depth_first_search"}, [
        "count connected components (islands)", "the fewest steps in an unweighted graph (BFS)",
        "multi-source BFS (rotting oranges)", "a grid as a graph with direction arrays",
        "model the problem as a graph: states as nodes", "detect a cycle"]),
    ("topological-sort", "Topological Sort", ["graphs"], "B", [12], ["topological-sort"], {"topological_sort"}, [
        "Kahn's algorithm with in-degrees", "detect a cycle with a topological order",
        "DFS post-order", "the longest path in a DAG (scheduling with durations)"]),
    ("union-find", "Union-Find", ["graphs"], "B", [14], ["union-find"], {"union_find"}, [
        "connected components as edges arrive", "find the redundant edge",
        "union by rank and path compression", "union-find that carries extra data (sizes, weights)",
        "process edges in sorted order (Kruskal, offline queries)"]),
    ("shortest-paths", "Shortest Paths", ["graphs", "heap"], "B", [14], ["shortest-path", "dijkstra", "bellman-ford"], {"shortest_path"}, [
        "Dijkstra with a heap", "0-1 BFS", "Bellman-Ford and at most k edges",
        "a minimax path (minimum effort)", "Dijkstra over states (node plus extra)"]),
    ("backtracking", "Backtracking", ["trees"], "B", [15], ["backtracking", "subsets", "permutations", "pruning"], {"backtracking"}, [
        "choose, explore, un-choose", "subsets (include or exclude)", "permutations with a used array",
        "combinations with a start index, skipping duplicates", "search a grid for a word", "prune early"]),
    ("dp-1d", "1-D Dynamic Programming", ["backtracking"], "B", [16, 17], ["dynamic-programming", "dp-1d", "memoization", "kadane", "lis", "counting-dp"],
     {"dynamic_programming"}, [
        "recursion, then memo, then table (climbing stairs)", "take or skip on a line (house robber)",
        "the minimum cost to reach a target (fewest coins)", "count the ways (decode ways)",
        "DP over prefixes with a dictionary (word break)", "Kadane: the best subarray ending here",
        "the longest increasing subsequence"]),
    ("knapsack", "Knapsack", ["dp-1d"], "C", [20], ["knapsack", "unbounded-knapsack"], {"dynamic_programming"}, [
        "0/1 knapsack: take or skip under a capacity", "subset sum: can I make exactly T",
        "exactly W versus at most W (the initial values)", "unbounded: each item any number of times (fewest coins)",
        "count combinations versus orderings (loop order)", "a disguise: +/- signs to reach T becomes subset sum",
        "partition into two sets with the smallest difference", "two resources at once (ones and zeroes)",
        "bounded copies, or swap the DP dimension when the capacity is huge"]),
    ("dp-2d", "2-D DP: Grids & Strings", ["dp-1d"], "C", [20], ["dp-2d", "dp-strings"], {"dynamic_programming"}, [
        "paths and costs on a grid", "the longest common subsequence", "edit distance",
        "palindromes: DP over (i, j) of one string", "design the state for two sequences"]),
    ("bits-math", "Bits & Maths", ["arrays-hashing"], "C", [21], ["bit-manipulation", "xor-tricks", "math", "number-theory", "modular-arithmetic"],
     {"bit_manipulation", "math"}, [
        "XOR cancels pairs", "a bitmask as a set", "count bits and powers of two",
        "gcd, lcm and modular arithmetic", "primes and a sieve"]),
    ("segment-tree", "Segment Trees", ["prefix-sums", "binary-search"], "C", [27], ["segment-tree", "fenwick-tree"], {"segment_tree"}, [
        "point update and range query", "a Fenwick tree for prefix sums", "range update with lazy propagation",
        "coordinate compression before counting"]),
    ("interval-dp", "Interval & Game DP", ["dp-2d"], "C", [28], ["partition-dp", "game-dp", "tree-dp"], {"dynamic_programming"}, [
        "DP over an interval (i, j) with a split point", "a two-player game: best score difference",
        "DP on a tree (choose or skip a node)", "merge stones / burst balloons style"]),
]
PHASES = {"A": ("OA core", "What online assessments ask most. Learn these first."),
          "B": ("Interview core", "Rarer in OAs, but the backbone of phone screens and onsites."),
          "C": ("Depth", "Once the core is automatic.")}
BAD_TOPIC = {"concurrency", "database"}
BAD_TITLE = re.compile(r"scratch|classifier|neural|regression|gradient|transformer|tokeni[sz]|goroutine|thread|mutex|\bsql\b|pandas|llm", re.I)
EXCLUDE = {"amazon-count-special-substrs", "amazon-find-first-index-where-prefix-sum-becomes-non-positive",
           "uber-counting-segments-after-house-removals", "tiktok-get-server-index"}


def order():
    """Prerequisites first; among what is unlocked, the declared (OA-first) sequence."""
    ids = [n[0] for n in NODES]
    parents = {n[0]: n[2] for n in NODES}
    done, out = set(), []
    while len(out) < len(ids):
        for i in ids:
            if i not in done and all(p in done for p in parents[i]):
                done.add(i); out.append(i); break
        else:
            raise SystemExit("the tree has a cycle")
    return out


def load_bank():
    c = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
    try:
        verified = {k for k, v in json.load(open(os.path.join(HERE, "solutions", "VERIFIED.json")))["problems"].items() if v.get("ok")}
    except (OSError, ValueError):
        verified = set()
    fixed = {f[:-5] for f in os.listdir(os.path.join(HERE, "fixes")) if f.endswith(".json") and f != "khatt.json"}
    P = {}
    for pid, d in c.execute("SELECT id, detail_json FROM problems"):
        d = json.loads(d or "{}")
        if d.get("practiceFormat", "algorithm") != "algorithm" or pid in EXCLUDE:
            continue
        st = re.sub(r"<[^>]+>", " ", d.get("problemStatement") or "")
        st = re.sub(r"\s+", " ", st).strip()
        P[pid] = dict(id=pid, title=d.get("title") or pid, company=d.get("company") or "", diff=(d.get("difficulty") or "medium").lower(),
                      oa="OA" in (d.get("problemTypes") or []), last=max(d.get("lastSeen") or [""]), seen=d.get("seenCount") or 1,
                      stlen=len(st), snippet=st[:280], imgs=len(d.get("sourceImages") or []), ex=len(d.get("examples") or []),
                      tags=set(d.get("topics") or []), verified=pid in verified, fixed=pid in fixed)
    index = json.load(open(os.path.join(HERE, "topics", "INDEX.json")))
    by_problem = index.get("byProblem", {})
    sizes = {t["slug"]: t.get("count", 0) for t in index["topics"]}
    return P, by_problem, sizes


def quality(p):
    if (p["stlen"] < 200 and not p["imgs"] and not p["fixed"]) or BAD_TOPIC & p["tags"] or BAD_TITLE.search(p["title"]):
        return None
    q = (3 if p["fixed"] else 0) + (3 if p["verified"] else 0) + (1.5 if p["oa"] else 0) + (1 if p["company"] == "Amazon" else 0)
    q += (1 if p["last"] >= "2025-06-01" else 0) + min(2, math.log2(p["seen"])) + (1 if p["ex"] >= 2 else 0)
    return q


def pools(argv):
    P, by_problem, sizes = load_bank()
    node_ch = {n[0]: set(n[5]) for n in NODES}
    node_tags = {n[0]: n[6] for n in NODES}
    # every problem goes to the ONE node it fits most specifically, so no two curators share a problem
    assign = collections.defaultdict(list)
    for pid, p in P.items():
        if quality(p) is None:
            continue
        chs = set(by_problem.get(pid, []))
        best = None
        for nid in node_ch:
            hit = chs & node_ch[nid]
            if hit:
                spec = min(sizes.get(h, 10 ** 6) for h in hit)           # the rarest matching chapter
            elif p["tags"] & node_tags[nid] and nid not in ("knapsack", "dp-2d", "interval-dp", "bst", "monotonic-stack", "bs-answer"):
                spec = 10 ** 5 + sum(1 for x in P.values() if False)      # a tag match only: a weaker claim
            else:
                continue
            if best is None or spec < best[0]:
                best = (spec, nid)
        if best:
            assign[best[1]].append(pid)
    os.makedirs(os.path.join(DIR, "pools"), exist_ok=True)
    for n in NODES:
        nid = n[0]
        ranked = sorted(assign.get(nid, []), key=lambda pid: -quality(P[pid]))[:110]
        lines = ["NODE %s: %s" % (nid, n[1]), "TECHNIQUES:"] + ["  - " + t for t in n[7]] + [
            "CANDIDATES (%d of %d, best first). Columns: id | difficulty | company | OA | solution verified | repaired | title :: start of statement"
            % (len(ranked), len(assign.get(nid, [])))]
        for pid in ranked:
            p = P[pid]
            lines.append("%s | %s | %s | %s | %s | %s | %s :: %s" % (
                pid, p["diff"], p["company"][:18], "OA" if p["oa"] else "-", "V" if p["verified"] else "-",
                "R" if p["fixed"] else "-", p["title"], p["snippet"]))
        open(os.path.join(DIR, "pools", nid + ".txt"), "w").write("\n".join(lines) + "\n")
        print("%-18s %4d candidates (%d written)" % (nid, len(assign.get(nid, [])), len(ranked)))
    return 0


def build(argv):
    P, _, _ = load_bank()
    nodes_out, seen = [], set()
    khatt_old = json.load(open(KHATT))
    slots = collections.defaultdict(list)
    for pid, v in khatt_old.items():
        slots[v["week"]].append(v["day"])
    DAYO = {d: i for i, d in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "optional"])}
    for w in slots:
        slots[w].sort(key=lambda d: DAYO.get(d, 9))
    rank = {nid: i + 1 for i, nid in enumerate(order())}
    defs = {n[0]: n for n in NODES}
    for nid in order():
        n = defs[nid]
        path = os.path.join(DIR, "nodes", nid + ".json")
        ladder = []
        if os.path.exists(path):
            for item in json.load(open(path)).get("ladder", []):
                if item.get("id") in P and item["id"] not in seen:
                    seen.add(item["id"]); ladder.append(item)
        nodes_out.append(dict(id=nid, title=n[1], parents=n[2], phase=n[3], order=rank[nid], weeks=n[4],
                              chapters=n[5], techniques=n[7], ladder=ladder))
    # KHATT: a week's slots are shared by its nodes, filled from the head of each ladder
    by_week = collections.defaultdict(list)
    for nd in nodes_out:
        for w in nd["weeks"]:
            by_week[w].append(nd)
    khatt = {pid: v for pid, v in khatt_old.items() if v["week"] not in by_week}
    for w, nds in sorted(by_week.items()):
        days = slots.get(w, [])
        if not days or not all(nd["ladder"] for nd in nds):
            for pid, v in khatt_old.items():          # an uncurated week keeps what it had
                if v["week"] == w:
                    khatt[pid] = v
            continue
        # how far into each ladder this week starts: a node spanning two weeks continues where it stopped
        picks, k = [], len(days)
        share = [k // len(nds) + (1 if i < k % len(nds) else 0) for i in range(len(nds))]
        for nd, s in zip(nds, share):
            # only this node's own earlier weeks count (not practice weeks it lent rungs to)
            prior = sum(1 for pid, v in khatt.items() if v.get("node") == nd["id"] and v["week"] in nd["weeks"] and v["week"] < w)
            picks += [(nd, it["id"]) for it in nd["ladder"][prior:prior + s]]
        for (nd, pid), day in zip(picks, days):
            khatt[pid] = {"week": w, "day": day, "label": nd["title"], "node": nd["id"]}
    # a practice week that lost a problem to a ladder gets it back: an unscheduled practice or
    # stretch rung from a topic already taught by then, taking topics in turn
    lost = [(v["week"], v["day"]) for pid, v in khatt_old.items()
            if v["week"] not in by_week and khatt.get(pid, {}).get("week") != v["week"]]
    for w, day in sorted(lost, key=lambda x: (x[0], DAYO.get(x[1], 9))):
        taught = [nd for nd in nodes_out if nd["ladder"] and max(nd["weeks"]) < w]
        taught.sort(key=lambda nd: sum(1 for v in khatt.values() if v["week"] == w and v.get("node") == nd["id"]))
        for nd in taught:
            spare = [it for it in nd["ladder"] if it.get("level") != "core" and it["id"] not in khatt]
            if spare:
                khatt[spare[0]["id"]] = {"week": w, "day": day, "label": nd["title"], "node": nd["id"]}
                break
    out = dict(phases={k: {"title": v[0], "about": v[1]} for k, v in PHASES.items()}, nodes=nodes_out)
    json.dump(out, open(os.path.join(DIR, "ROADMAP.json"), "w"), indent=1)
    json.dump(dict(sorted(khatt.items(), key=lambda kv: (kv[1]["week"], DAYO.get(kv[1]["day"], 9), kv[0]))), open(KHATT, "w"), indent=1)
    print("roadmap: %d nodes, %d curated, %d problems; KHATT %d"
          % (len(nodes_out), sum(1 for x in nodes_out if x["ladder"]), sum(len(x["ladder"]) for x in nodes_out), len(khatt)))
    return 0


def status(argv):
    P, _, _ = load_bank()
    for nid in order():
        path = os.path.join(DIR, "nodes", nid + ".json")
        if not os.path.exists(path):
            print("%-18s not curated" % nid); continue
        lad = json.load(open(path)).get("ladder", [])
        print("%-18s %2d problems, %2d verified, %2d repaired" % (nid, len(lad), sum(P.get(x["id"], {}).get("verified", False) for x in lad),
                                                                  sum(P.get(x["id"], {}).get("fixed", False) for x in lad)))
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    sys.exit({"pools": pools, "build": build, "status": status}.get(cmd, lambda a: print(__doc__) or 2)(sys.argv[2:]))

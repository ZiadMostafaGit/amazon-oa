# Persistent Data Structures

> Persistence is not about disks. It is the discipline of never overwriting
> anything: an update produces a new version and leaves every old one readable,
> and the trick that makes it affordable is that the new version keeps almost
> all of the old one's memory.

## When you reach for it

You reach for persistence when a query names a *moment* rather than just a key.
"What was the value of `x` at snapshot 7?" is a different question from "what is
the value of `x`?", and a plain dictionary can answer only the second, because
the write that produced the current value destroyed the previous one.

One hundred and twelve problems in this bank sit on this topic, #32 of 150. They
come in a small number of recognisable shapes:

- **Versioned key-value stores.** *Globally Versioned Key-Value Store* bumps a
  global version on every `SET` and asks for the value at "the greatest global
  version less than or equal to `version`". *Snapshot Map with Sparse Version
  History* is the same with explicit `SNAPSHOT`s and a ban on duplicating
  unchanged keys.
- **Snapshot collections.** *Versioned Snapshot Set* captures the whole set and
  later dumps it; *Snapshot Set Iterator* hands out an iterator whose view stays
  frozen while the set keeps changing under it.
- **Versioned graphs.** *Versioned Social Network*, *Versioned Followers and
  Followees* and *Versioned Friend Recommendations* all say in the statement that
  a snapshot must not copy the graph — keep a change history per edge.
- **Version-numbered records.** *Cloud Storage File Versioning*, *Versioned
  Recipe System*, *Versioned In-Memory File System*: documents that accumulate
  numbered versions with `ROLLBACK`, `BACKUP` and `RECOVER`.
- **Branching history.** *Versioned Key-Value Store with Commits* rolls back and
  then "later writes form a new working branch"; *Versioned Recipe Shopping
  Cart*'s `checkout` restores a version and discards everything after it. The
  version axis is a tree, not a line.

The tool is wrong when only the newest state is ever read: history you never
query is pure overhead. It is also wrong when the word *version* is a red
herring, which happens often enough to deserve a warning. *Compare Version
Numbers* is string [[parsing|parsing]]; *First Bad Version* is [[binary-search]]
over a monotone predicate; *Closest Version Date* is a nearest-neighbour search.
None of them needs anything to remember its past. The trigger is not the noun
"version" — it is a **query that takes a version as an argument**.

## The idea

Mutation destroys. Versioning appends.

That single sentence is the whole topic, and everything below is a way of making
"append" cheap. Two mechanisms do almost all the work.

**Fat nodes.** Instead of one slot per key holding the current value, give each
key a *list of stamped values*: `[(1, "a"), (4, "b"), (9, "c")]`, versions
ascending. A write appends. A snapshot is not a copy of anything — it is just
the current version number, remembered. Reading key `k` at version `v` means
finding the last entry whose stamp is at most `v`, which is a predecessor search
in a sorted list, i.e. [[binary-search]].

The economy is easiest to see by asking what a snapshot costs when a key was not
touched. Nothing at all: the key's list is unchanged, and "no entry between `v`
and `v+1`" already means "unchanged between `v` and `v+1`". A million untouched
keys cost a million times zero.

<svg viewBox="0 0 640 230" role="img" aria-label="two keys with stamped value histories along a version axis, and a query at version four resolving to the entry stamped three">
  <g>
    <text x="14" y="62">key a</text>
    <text x="14" y="132">key b</text>
    <line x1="70" y1="190" x2="600" y2="190"/>
    <text x="100" y="212" text-anchor="middle">v1</text>
    <text x="190" y="212" text-anchor="middle">v2</text>
    <text x="280" y="212" text-anchor="middle">v3</text>
    <text x="370" y="212" text-anchor="middle">v4</text>
    <text x="460" y="212" text-anchor="middle">v5</text>
    <text x="550" y="212" text-anchor="middle">v6</text>
    <line x1="100" y1="185" x2="100" y2="195"/>
    <line x1="190" y1="185" x2="190" y2="195"/>
    <line x1="280" y1="185" x2="280" y2="195"/>
    <line x1="370" y1="185" x2="370" y2="195"/>
    <line x1="460" y1="185" x2="460" y2="195"/>
    <line x1="550" y1="185" x2="550" y2="195"/>
    <rect class="fill" x="74" y="38" width="52" height="34" rx="5"/>
    <text x="100" y="61" text-anchor="middle">1</text>
    <rect class="fill" x="254" y="38" width="52" height="34" rx="5"/>
    <text x="280" y="61" text-anchor="middle">3</text>
    <rect x="164" y="108" width="52" height="34" rx="5"/>
    <text x="190" y="131" text-anchor="middle">2</text>
    <rect x="344" y="108" width="52" height="34" rx="5"/>
    <text x="370" y="131" text-anchor="middle">del</text>
    <line x1="370" y1="185" x2="370" y2="30" stroke-dasharray="5 5"/>
    <text x="392" y="26">get_at(a, 4)</text>
    <line x1="366" y1="30" x2="310" y2="48"/>
    <line x1="310" y1="48" x2="324" y2="46"/>
    <line x1="310" y1="48" x2="322" y2="56"/>
    <text x="70" y="168">nothing is stored at the versions where a key did not change</text>
  </g>
</svg>

**Path copying.** Fat nodes suit queries that name one key. When a query wants a
whole structure — a set to iterate, a tree to search — you want a *root pointer
per version*. Build the collection as a tree; to change one element, rebuild only
the nodes on the root-to-leaf path and let the new nodes point at the *old*
untouched subtrees. The new root describes the new state, the old root still
describes the old one, and they share everything but that path.

<svg viewBox="0 0 600 270" role="img" aria-label="a four-level binary tree with the four nodes on one root-to-leaf path highlighted as newly copied, the other eleven shared">
  <g>
    <circle class="fill" cx="295" cy="35" r="15"/>
    <circle class="fill" cx="155" cy="95" r="15"/>
    <circle cx="435" cy="95" r="15"/>
    <circle cx="85" cy="155" r="15"/>
    <circle class="fill" cx="225" cy="155" r="15"/>
    <circle cx="365" cy="155" r="15"/>
    <circle cx="505" cy="155" r="15"/>
    <circle cx="50" cy="215" r="12"/>
    <circle cx="120" cy="215" r="12"/>
    <circle cx="190" cy="215" r="12"/>
    <circle class="fill" cx="260" cy="215" r="12"/>
    <circle cx="330" cy="215" r="12"/>
    <circle cx="400" cy="215" r="12"/>
    <circle cx="470" cy="215" r="12"/>
    <circle cx="540" cy="215" r="12"/>
    <line x1="283" y1="44" x2="167" y2="86"/>
    <line x1="307" y1="44" x2="423" y2="86"/>
    <line x1="144" y1="105" x2="96" y2="145"/>
    <line x1="166" y1="105" x2="214" y2="145"/>
    <line x1="424" y1="105" x2="376" y2="145"/>
    <line x1="446" y1="105" x2="494" y2="145"/>
    <line x1="76" y1="166" x2="59" y2="205"/>
    <line x1="94" y1="166" x2="111" y2="205"/>
    <line x1="216" y1="166" x2="199" y2="205"/>
    <line x1="234" y1="166" x2="251" y2="205"/>
    <line x1="356" y1="166" x2="339" y2="205"/>
    <line x1="374" y1="166" x2="391" y2="205"/>
    <line x1="496" y1="166" x2="479" y2="205"/>
    <line x1="514" y1="166" x2="531" y2="205"/>
    <text x="295" y="255" text-anchor="middle">one write on 8 leaves: 4 new nodes, 11 shared with the previous version</text>
  </g>
</svg>

Both are the same idea from two ends. Fat nodes share by *omission*: an absent
entry means unchanged. Path copying shares by *reference*: a reused pointer means
unchanged. Pick by what the query asks for — one cell, or the whole collection.

## Worked by hand

Take *Globally Versioned Key-Value Store*: `SET` bumps a global counter and
stores at that counter; `GET_AT key version` returns the value at the greatest
stored version `<= version`, or `NULL`. Run six operations. The state is one
list of `(version, value)` pairs per key, plus the counter.

| step | operation | version | `a` history | `b` history | output |
| --- | --- | --- | --- | --- | --- |
| 1 | `SET a 1` | 1 | `[(1,"1")]` | `[]` | — |
| 2 | `SET b 2` | 2 | `[(1,"1")]` | `[(2,"2")]` | — |
| 3 | `SET a 3` | 3 | `[(1,"1"),(3,"3")]` | `[(2,"2")]` | — |
| 4 | `GET_AT a 2` | 3 | unchanged | unchanged | `1` |
| 5 | `GET_AT a 0` | 3 | unchanged | unchanged | `NULL` |
| 6 | `GET_AT b 9` | 3 | unchanged | unchanged | `2` |

Four things in that table are worth a second look, and none of them are visible
in the code.

**Step 4 is the whole topic in one row.** Nothing was ever stored at version 2
for key `a`. The answer `1` comes from the entry at version 1, because the
absence of an entry between 1 and 3 *is* the statement "`a` did not change".
Storage is proportional to the number of writes, not to the number of versions.

**Step 5 is the case that crashes.** The query version precedes every entry, so
the predecessor search returns index −1 — and in Python `history[-1]` is not an
error, it is the *most recent* entry. A missing guard silently turns "this key
did not exist yet" into "here is its final value", and only on queries aimed
before a key's first write. That missing `if i >= 0` is the commonest bug here.

**Step 6 asks for a version in the future.** Version 9 does not exist yet, and
the predecessor search handles it with no special case: the greatest stamp at
most 9 is 2. A query past the end is the same operation as one in the middle,
which is why this formulation needs so few branches.

**The histories are append-only, and that is an assumption, not a fact.** Each new
stamp beats every existing one *because the counter only goes up*. In *Versioned
Key-Value Store with Suffix Truncation* the caller supplies the version, so writes
land in the middle and the list must be kept sorted by insertion instead. Which
of the two you are in decides whether `append` is legal.

## Why it is correct

What needs proving is not that the code runs but that the structure is
*persistent*: a query against version `v` must return exactly what an ordinary
mutable store would have returned if it had been stopped at `v` and never
touched again. That is a statement about the whole history, so it wants an
invariant and induction over the write sequence.

:::proof A fat-node store answers every version exactly

**Setup.** Let the writes be `w₁, …, w_m` in order, where `w_t` assigns value
`x_t` to key `k_t` (a delete assigns the distinguished value `⊥`). Define the
*reference state* `S_t` by `S_0(k) = ⊥` for all `k`, and `S_t = S_{t-1}` except
that `S_t(k_t) = x_t`: this is the map an ordinary dictionary would hold after
`t` writes, and it is what we must reproduce. The implementation keeps, per key
`k`, a list `H[k]` of pairs `(version, value)`, and a counter `V`.

**Invariant.** After `t` writes, for every key `k`:

- **(I1)** the version components of `H[k]` are strictly increasing, and `V = t`;
- **(I2)** `(s, x) ∈ H[k]` if and only if `1 <= s <= t`, `k_s = k` and `x = x_s` —
  the list holds exactly the writes aimed at `k`, and nothing else;
- **(I3)** for every `v` with `0 <= v <= t`, `S_v(k)` equals the value of the
  entry of `H[k]` with the greatest version `<= v`, and `⊥` when no entry
  qualifies.

**Base case (`t = 0`).** Every `H[k]` is empty and `V = 0`. (I1) is vacuous,
(I2) is vacuous, and for (I3) the only `v` is 0, no entry qualifies, and
`S_0(k) = ⊥`. Holds.

**Inductive step.** Assume the invariant after `t` writes and perform `w_{t+1}`,
which sets `V = t + 1` and appends `(t + 1, x_{t+1})` to `H[k_{t+1}]`.

*(I1)* Every existing version in every list is at most `t` by (I2), and the new
one is `t + 1`, so appending keeps the list strictly increasing, and `V = t + 1`.

*(I2)* Exactly one pair was added, to exactly the key that was written, carrying
exactly that version and value. No other list changed.

*(I3)* Fix a key `k` and a version `v <= t + 1`.

- If `v <= t`, the appended entry has version `t + 1 > v`, so it is not a
  candidate for "greatest version `<= v`" and no other entry moved: the selected
  entry is the one selected before the write. `S_v(k)` did not change either,
  since `S_v` depends only on `w₁ … w_v`. The hypothesis carries over.
- If `v = t + 1` and `k = k_{t+1}`, the new entry has the largest version in the
  list and it is `<= v`, so it is the one selected; its value is `x_{t+1}`,
  which is exactly `S_{t+1}(k_{t+1})` by the definition of `S`.
- If `v = t + 1` and `k ≠ k_{t+1}`, then `H[k]` is untouched, so the selected
  entry is the same as the one selected for `v = t`; by the hypothesis that
  value is `S_t(k)`, and by the definition of `S`, `S_{t+1}(k) = S_t(k)` because
  the write missed `k`. Equal, as required.

**The query.** `get_at(k, v)` wants the entry of `H[k]` with the greatest version
`<= v`. By (I1) the list is sorted, so `bisect_right(versions, v) - 1` is exactly
that index: `bisect_right` returns the number of entries with version `<= v` —
the count of "yes" answers to a monotone predicate, proved in [[binary-search]] —
and subtracting one indexes the last of them, or gives `-1` when the count is
zero. By (I3) the returned value is `S_v(k)`.

**Conclusion.** For every key `k` and version `v`, the structure returns
`S_v(k)` — what the mutable store would have held after exactly `v` writes. Since
no operation removes or rewrites an entry, this stays true for the rest of the
run: the past is immutable. ∎
:::

Now the assumptions, because that is where the bugs live.

- **Versions are totally ordered and writes arrive in increasing order.** Used in
  (I1) to justify `append`, and in (I3) to argue the new entry cannot be selected
  by an older query. If the caller supplies versions (*Versioned Key-Value Store
  with Suffix Truncation*), the sorted order must be re-established by insertion,
  and the "old queries are unaffected" argument needs restating — inserting in
  the middle *can* change what an older query sees, which is the point of that
  problem.
- **A delete is a write, not a removal.** The proof's `⊥` is a stored value. If
  `delete` instead popped the key's history, (I2) would break and a query before
  the delete would return `⊥` where the mutable store held a real value. Deletes
  must be tombstones.
- **Entries are never mutated after being written.** Nothing in the induction
  re-examines an old entry, so nothing repairs one that has been edited.
- **Snapshot ids and write versions live on the same axis.** (I3) compares a
  query's `v` against stored stamps, which is meaningless if a second counter
  advances at a different rate. Stamp writes with the snapshot counter, or map
  ids into the write-version space once.
- **Every change is recorded, and only real changes are.** "Absent means
  unchanged" is an *iff*. A skipped write makes a key look unchanged when it was
  not; a recorded no-op is harmless for correctness but violates the explicit
  rule in *Snapshot Map with Sparse Version History* that repeating a `PUT` with
  the same value must not add a version.

Path copying has a shorter proof with one dangerous assumption. Its invariant is:
*the tree rooted at `root_v` represents `S_v`, and no node reachable from any
`root_u` with `u < v` is ever written to.* An update rebuilds the nodes along one
root-to-leaf path and reuses the sibling pointers; by induction on the path
length each rebuilt node has the correct children, so the new root represents
`S_v` with one element changed. The second clause is the whole safety property,
and it survives only because *every* node on the path is freshly allocated. One
in-place assignment below an old root — the optimisation that looks free because
"this node is only used here" — corrupts every earlier version sharing it, at
once.

## What it costs

Start with the alternative, because the derivation is the argument for the
technique existing at all.

**Snapshot by full copy.** With `s` snapshots over `n` keys, copying costs `Θ(n)`
per snapshot and `Θ(s·n)` in total, in time and space. *Snapshot Map with Sparse
Version History* allows 10⁶ distinct keys and 10⁵ snapshots: `s·n = 10¹¹`
entries, which finishes on no machine — yet the same statement caps operations at
2·10⁵. The gap between the *product* `s·n` and the *sum* of the operations is why
the statement tells you to store only per-key changes.

**Fat nodes.** Every write appends one entry and nothing is removed, so after `m`
writes the stored entries number exactly `m`: `Σ_k |H[k]| = m`. Space is
`Θ(m + K)` for `K` distinct keys, independent of the snapshot count. A write is
an `append` — `O(1)` amortised, by the doubling argument in
[[amortized-analysis]] — plus an expected-`O(1)` hash lookup ([[hash-tables]]).
A version read costs the predecessor search, `Θ(log h_k)` where `h_k <= m` is the
number of writes to *that* key. So `m` writes and `q` version queries cost
`Θ(m + q log m)` time and `Θ(m + K)` space: a few million steps at 2·10⁵
operations.

**Path copying on a balanced tree.** One update rebuilds the nodes on one
root-to-leaf path. Writing `C(n)` for the nodes allocated when updating a
subtree of `n` leaves,

```
C(1) = 1,    C(n) = C(n/2) + 1
```

because you rebuild the current node and recurse into exactly one child. The
solution is `C(n) = log₂ n + 1`. So `m` versions of an `n`-element structure cost
`Θ(m log n)` time and space, against `Θ(m·n)` for full copies — a factor of
`n / log n`, which at `n = 10⁶` is about fifty thousand. The runnable code below
checks the `log₂ n + 1` count exactly, by counting distinct node objects across
all versions.

Two refinements. Branching factor `b` gives depth `log_b n` and `b` slots copied
per level, so `b · log_b n` words per update; real persistent vectors use
`b = 32` because the copies are contiguous — depth 4 at `n = 10⁶`, about 128
words. And balance matters: path copying on an unbalanced
[[bst|binary search tree]] costs the *height*, which can be `n`, which is why
persistent search trees are built on [[balanced-bst|balanced trees]].

**The costs people forget.**

- *The read side.* `q log m` can exceed `m`; few writes and many historical reads
  means the searches, not the storage, are the bottleneck.
- *Materialising a whole version.* No representation makes "dump every element of
  snapshot 7" cheaper than the size of snapshot 7. That is why *Versioned
  Snapshot Set* bounds the *sum* of values returned across all `GET_SNAPSHOT`
  calls at 2·10⁵ rather than bounding the snapshot count — read that kind of
  constraint as a statement about the intended algorithm.
- *Memory is cumulative.* Old versions are never collected, so peak memory is the
  integral of the history, not the current state's size. Only an explicit
  truncation rule lets you reclaim.
- *Object overhead in Python.* Two parallel lists — versions and values — beat a
  list of small objects and let `bisect` work on plain integers.

## The implementation

```python run
import random
from bisect import bisect_right

NULL = "<NULL>"


class VersionedStore:
    """Every write gets the next global version; nothing is overwritten.
    get_at(key, v) answers as the store stood after exactly v writes."""

    def __init__(self):
        self.vers = {}                       # key -> ascending version stamps
        self.vals = {}                       # key -> values, parallel to vers
        self.version = 0

    def _write(self, key, value):
        self.version += 1
        if key not in self.vers:
            self.vers[key], self.vals[key] = [], []
        self.vers[key].append(self.version)  # legal only because stamps rise
        self.vals[key].append(value)
        return self.version

    def put(self, key, value):
        return self._write(key, value)

    def delete(self, key):
        return self._write(key, NULL)        # a tombstone, never a removal

    def get_at(self, key, version):
        vs = self.vers.get(key)
        if not vs:
            return NULL
        i = bisect_right(vs, version) - 1    # last stamp <= version
        return self.vals[key][i] if i >= 0 else NULL

    def get(self, key):
        return self.get_at(key, self.version)


s = VersionedStore()
for key, value in [("a", "1"), ("b", "2"), ("a", "3")]:
    print("put %s=%s -> version %d" % (key, value, s.put(key, value)))
print("delete b   -> version %d" % s.delete("b"))
print("history of a:", list(zip(s.vers["a"], s.vals["a"])))
print("a at v0,v1,v2,v3:", [s.get_at("a", v) for v in range(4)])
assert [s.get_at("a", v) for v in range(4)] == [NULL, "1", "1", "3"]
assert s.get_at("b", 3) == "2" and s.get_at("b", 4) == NULL and s.get("b") == NULL
print("entries stored:", sum(len(v) for v in s.vers.values()), "= number of writes")

rng = random.Random(5)
for _ in range(300):                         # cross-check against full copies
    st, truth = VersionedStore(), [{}]
    for _ in range(rng.randint(0, 30)):
        k, cur = rng.choice("abcd"), dict(truth[-1])
        if rng.random() < 0.3:
            st.delete(k)
            cur.pop(k, None)
        else:
            v = str(rng.randrange(5))
            st.put(k, v)
            cur[k] = v
        truth.append(cur)
    for v in range(len(truth)):
        for k in "abcd":
            assert st.get_at(k, v) == truth[v].get(k, NULL), (v, k)
print("300 random histories: every key at every version matches a full copy")
```

Three lines carry the weight. `append` rather than `insort` is legal only because
the global counter guarantees the new stamp is the largest — the proof's
assumption written as code. `bisect_right` rather than `bisect_left` is what lets
a query at a version where a write happened see *that* write. And
`if i >= 0 else NULL` stops `self.vals[key][-1]` from quietly returning the
newest value for a query aimed before the key existed.

The cross-check is the part worth stealing. A persistent structure always has an
obvious slow reference implementation — a full copy per version — so "matches the
copies at every version" is testable exhaustively on small random inputs. Most
persistence bugs are invisible on the latest version and show up only on some old
one, which a sweep over all `v` catches and a hand-written example does not.

Here is path copying, with the sharing counted rather than asserted:

```python run
SIZE = 8                                     # a persistent array of 8 slots


def build(lo, hi, fill):
    if hi - lo == 1:
        return ("leaf", fill)
    mid = (lo + hi) // 2
    return ("node", build(lo, mid, fill), build(mid, hi, fill))


def read(root, i):
    node, lo, hi = root, 0, SIZE
    while node[0] != "leaf":
        mid = (lo + hi) // 2
        node, lo, hi = (node[1], lo, mid) if i < mid else (node[2], mid, hi)
    return node[1]


def write(node, i, x, lo=0, hi=SIZE):
    """Return a NEW root. Only the nodes on the path to i are rebuilt; the
    sibling pointer on each level is reused, so the old root stays valid."""
    if hi - lo == 1:
        return ("leaf", x)
    mid = (lo + hi) // 2
    if i < mid:
        return ("node", write(node[1], i, x, lo, mid), node[2])
    return ("node", node[1], write(node[2], i, x, mid, hi))


def distinct_nodes(roots):
    seen, stack = {}, list(roots)
    while stack:
        nd = stack.pop()
        if id(nd) in seen:
            continue
        seen[id(nd)] = nd                    # keep a reference: ids must stay live
        if nd[0] == "node":
            stack.extend((nd[1], nd[2]))
    return len(seen)


roots = [build(0, SIZE, 0)]
for v, (i, x) in enumerate([(3, 30), (0, 10), (7, 70), (3, 33), (5, 50), (0, 11)]):
    roots.append(write(roots[-1], i, x))
    print("v%d after a[%d]=%-3d ->" % (v + 1, i, x),
          [read(roots[-1], j) for j in range(SIZE)])

print("v0 is still        ->", [read(roots[0], j) for j in range(SIZE)])
assert [read(roots[0], j) for j in range(SIZE)] == [0] * SIZE
assert read(roots[1], 3) == 30 and read(roots[3], 3) == 30 and read(roots[4], 3) == 33

total, full = distinct_nodes(roots), len(roots) * (2 * SIZE - 1)
print("distinct nodes over all %d versions: %d   (full copies would need %d)"
      % (len(roots), total, full))
assert total == (2 * SIZE - 1) + 6 * 4       # log2(8) + 1 = 4 new nodes per write
print("each write allocated exactly log2(8) + 1 = 4 nodes")
```

`write` never assigns into `node`; it *returns* a rebuilt tuple and passes the
untouched child straight through. Because nodes are tuples, Python will not let
you break the invariant by accident — immutability is the safety mechanism, not a
decoration. `distinct_nodes` makes the complexity claim executable: 15 nodes for
the first version, then exactly 4 per update.

## Variants you will meet

**Fat nodes with a per-key change log.** The default in this bank. *Versioned
Social Network* requires it outright: `FOLLOW`, `UNFOLLOW` and `SNAPSHOT` in
expected `O(1)`, a historical query in `O(log h)` where `h` is the number of
recorded changes for that one relationship, and `O(c)` total space. That
specification *is* the structure, spelled out.

**Path copying over a tree.** `O(log n)` per version, whole-structure views for
free. See [[trees]] and [[balanced-bst]].

**Persistent segment tree.** Path copying applied to a [[segment-tree]]: each
version is a root, and subtracting two roots node by node answers "what changed
between version `u` and version `v`" — the standard route to offline
range-`k`-th-smallest.

**Copy-on-write snapshots.** Copy the whole state, but only when snapshots are
rare and the state small. *Versioned In-Memory File System*'s `BACKUP` and
`RECOVER` are this: a backup returns the number of files saved and a recover
replaces the state wholesale, so the copy is both the storage and the answer.

**Operation log and replay.** Store the operations, not the states, and rebuild a
version by replaying the prefix. *Versioned Recipe Shopping Cart* asks for exactly
this — "store compact add/remove history rather than a complete cart snapshot for
every version" — the right call when the derived answer is cheap to recompute.

**Branching versions.** `ROLLBACK` that keeps the old versions alive turns the
version line into a tree. *Versioned Key-Value Store with Commits* says later
writes after a rollback "form a new working branch"; *Versioned Recipe Shopping
Cart*'s `checkout` truncates instead, discarding every later version. These are
different data models — a version *tree* versus a version *stack* — and reading
the statement carefully is the whole difference.

**Partial versus full persistence.** *Partial*: read any version, write only the
newest — every problem listed above, and the reason `append` works. *Full*:
write to any version, producing a branch; the append shortcut is gone.
*Confluent*: additionally merge two versions, the way version control does.
Interviews stop at partial.

**Rollback by undo journal.** If you only ever go *back*, in last-in-first-out
order, skip persistence: push an inverse operation on a stack and pop to undo.
Cheaper than everything above; a rollback [[union-find]] is the canonical example
and the engine behind offline dynamic connectivity.

**Immutable linked lists.** The degenerate case: `cons(x, tail)` is `O(1)`, fully
persistent and shares the whole tail, so a persistent stack is free
([[linked-list]]). A persistent *queue* needs the two-list trick, whose
amortisation breaks when an expensive state can be re-entered from an old
version — a caution about applying [[amortized-analysis]] where the past is
reachable.

**Versioned records that are not persistent at all.** *Cloud Storage File
Versioning* keeps numbered versions, but `DELETE_VERSION` renumbers every higher
one. History that can be edited is not history: that is an array of versions, and
the right structure is a list.

## Recognising it in a statement

Ordered by how far you should trust them.

1. **"Immutable snapshot", or "later updates never change an earlier
   snapshot".** Near-certain. *Versioned Snapshot Set* and *Versioned Social
   Network* both say it in those words.
2. **An explicit instruction not to copy.** "A snapshot must not copy the entire
   graph." "Store only per-key changes rather than copying unchanged values into
   every snapshot." The statement is naming the intended structure.
3. **A query signature that takes a version or snapshot id.** `GET_AT key
   version`, `IS_FOLLOWING u v snapshot_id`, `GET_SNAPSHOT id`. If the version is
   a *parameter*, you need history; if it is only ever an output, you may not.
4. **The phrase "the greatest version less than or equal to".** A predecessor
   search written in English: sorted per-key list plus [[binary-search]].
5. **A constraint asymmetry between the product and the sum.** Many keys, many
   snapshots, few operations. Compute `keys × snapshots`; if it dwarfs the
   operation count, copying is excluded by arithmetic alone.
6. **A stated complexity that names the history length.** *Versioned Friend
   Recommendations* asks for `O(log h)` per relationship query, `h` being that
   relationship's recorded changes. Only one structure has that bound.
7. **`BACKUP` / `RECOVER` / `COMMIT` / `ROLLBACK` / `CHECKOUT` vocabulary.**
   Suggestive only — check whether old versions survive the rollback. If they do
   not, an undo stack is enough.

The anti-signals, all of them real problems in this bank:

- **"Version" as a string to parse and compare.** *Compare Version Numbers* —
  [[parsing]] and nothing else.
- **"Version" as an index into a monotone predicate.** *First Bad Version* and
  *First Bad Version in a Monotone Array* — [[binary-search]]; the versions are
  labels on array positions and nothing is stored per version.
- **"Version" as a label on a data point.** *Closest Version Date* is a
  nearest-neighbour query on sorted dates.
- **Only the latest state is ever read.** The history is then dead weight; use a
  dictionary. Many [[design-data-structure|data structure design]] questions look
  versioned and are not.

## Traps

**Storing a reference to the live state as the snapshot.** Symptom: every snapshot
returns the final state, invisible until you query more than one.

**A shallow copy of nested state.** `dict(store)` copies the outer map and shares
the inner lists. Symptom: top-level keys right, nested values all current.

**`bisect_left` where `bisect_right` belongs.** Symptom: a query at a version
where a write happened returns the *previous* value. Because it is right
everywhere else, the failing cases are precisely the exact hits.

**No guard on the `-1` index.** Symptom: a query aimed before a key's first write
returns that key's newest value, with no exception at all. The most expensive
line to omit in this topic.

**Deleting a key by removing its history.** Symptom: a historical query straddling
the delete returns nothing, or the value from before it. Deletes are tombstones,
and the tombstone must be a value that cannot occur for real.

**Two counters on different clocks.** A snapshot id that advances only on
`SNAPSHOT` while version stamps advance on every write means the query's number
and the stored numbers mean different things. Symptom: correct until two writes
occur between consecutive snapshots.

**Recording writes that change nothing.** *Snapshot Map with Sparse Version
History* forbids it outright: repeating a `PUT` with the same current value must
not add a version. Symptom: wrong snapshot contents in the specific case where a
key is mutated and restored between two snapshots.

**Mutating a node reachable from an old root.** The path-copying failure. Symptom:
a version you never touched changes value — the most disorienting bug in the
family, because the corrupted version and the operation that corrupted it are
arbitrarily far apart.

**Rebuilding a whole snapshot to answer a one-key question.** Symptom: correct
answers, `O(n)` per query, a timeout only on the large tests.

```python run
from bisect import bisect_right, bisect_left

# 1. a snapshot that stores a reference instead of a copy
live = {"a": 1}
aliased, copied = [live], [dict(live)]
live["a"] = 2
aliased.append(live)
copied.append(dict(live))
print("aliased snapshots:", aliased, "<- snapshot 0 has been rewritten")
print("copied snapshots: ", copied)
assert aliased[0]["a"] == 2 and copied[0]["a"] == 1

# 2. predecessor search, three ways. key written at versions 2, 5 and 9.
vers, vals = [2, 5, 9], ["x", "y", "z"]


def correct(v):
    i = bisect_right(vers, v) - 1
    return vals[i] if i >= 0 else "<NULL>"


def with_bisect_left(v):
    i = bisect_left(vers, v) - 1              # misses the exact version
    return vals[i] if i >= 0 else "<NULL>"


def without_the_guard(v):
    return vals[bisect_right(vers, v) - 1]    # vals[-1] is the NEWEST value


print("at v=5 :", correct(5), "correct |", with_bisect_left(5), "from bisect_left")
print("at v=1 :", correct(1), "correct |", without_the_guard(1), "with no i>=0 guard")
assert correct(5) == "y" and with_bisect_left(5) == "x"
assert correct(1) == "<NULL>" and without_the_guard(1) == "z"
print("both wrong answers are plausible values, which is why they survive review")
```

Neither wrong answer raises an exception and neither looks absurd. That is the
character of the topic: failures are silent and confined to old versions, so the
defence is the exhaustive cross-check against full copies, not careful reading.

## What to memorise

The template, which should come out of your fingers without thought:

```python
from bisect import bisect_right

vers, vals, version = {}, {}, 0               # key -> stamps, key -> values

def put(key, value):
    global version
    version += 1
    vers.setdefault(key, []).append(version)
    vals.setdefault(key, []).append(value)

def get_at(key, v):
    vs = vers.get(key)
    if not vs:
        return NULL
    i = bisect_right(vs, v) - 1               # last stamp <= v
    return vals[key][i] if i >= 0 else NULL   # i < 0: the key did not exist yet
```

The sentence that turns a problem into it: *"Does a query name a version — and
is `keys × versions` far larger than the number of operations?"* If both, store
per-key change lists and let absence mean unchanged.

The habit: **never overwrite, and always guard the `-1`.** Every persistent
write is an append of a stamped value, including deletes, which append a
tombstone; every persistent read is a predecessor search whose empty case must
be handled before indexing.

Numbers worth carrying. Fat-node space is exactly the number of writes,
independent of the number of snapshots. Path copying allocates `log₂ n + 1`
nodes per version, so `m` versions cost `Θ(m log n)` instead of `Θ(m·n)` — about
a fifty-thousand-fold saving at `n = 10⁶`. A branching factor of 32 puts a
million elements four levels deep. And `10⁶ keys × 10⁵ snapshots = 10¹¹`, which
is the number that rules out copying in *Snapshot Map with Sparse Version
History* before you write a line.

## Check yourself

:::check
A snapshot is taken while a million keys sit in the store, and only three of them
have ever been written. Why does the snapshot cost `O(1)` rather than `O(10⁶)`,
and what exactly is being relied on?
--
The snapshot stores one integer: the current version number. Nothing is copied.

What is relied on is the *iff* in invariant (I2): an entry exists in `H[k]`
exactly when a write targeted `k`, so the absence of an entry between versions
`v` and `v+1` carries the information "key `k` did not change". A reader recovers
`S_v(k)` by searching back for the last recorded change; a key that never changed
has no entry to find, which the query handles as the `i < 0` case.

That is why the *iff* must hold in both directions. If a write were ever skipped,
absence would also mean "we forgot", and the two are indistinguishable at read
time.
:::

:::check
Someone says: "persistence is over-engineering — I'll append `dict(store)` to a
list on every snapshot. Python's `dict` copy is written in C and it is fast."
Where are they wrong, and is there a case where they are right?
--
Two errors, one of scale and one of correctness.

*Scale.* `dict(store)` is `Θ(n)` no matter how fast the constant is. With
`s` snapshots the total is `Θ(s·n)`, and *Snapshot Map with Sparse Version
History* permits `s = 10⁵` and `n = 10⁶`, so `s·n = 10¹¹` entries — not a
constant-factor problem, an arithmetic impossibility. The fat-node cost is
`Θ(m)` with `m <= 2·10⁵` writes: six orders of magnitude apart.

*Correctness.* `dict(store)` is shallow, so if values are lists or sets — a
versioned graph's adjacency — every snapshot shares the inner objects and shows
the newest contents.

They are right when snapshots are rare, the state is small, and a snapshot is
*restored* wholesale rather than queried per key. *Versioned In-Memory File
System*'s `BACKUP`/`RECOVER` is that shape: the copy is both the storage and the
answer.
:::

:::check
`get_at(key, v)` uses `bisect_right(vers, v) - 1`. Derive why `bisect_left`
would be wrong, and name the only inputs on which the two disagree.
--
`bisect_right(vers, v)` counts stamps `<= v`; `bisect_left(vers, v)` counts
stamps `< v`. We want the greatest stamp `<= v`, whose index is
(count of stamps `<= v`) − 1 — the `bisect_right` form.

They differ exactly when `v` itself appears in `vers` — that is, when a write
happened at precisely the version being queried. Then `bisect_left` excludes that
write and returns the value from before it. On `vers = [2, 5, 9]`, `get_at(·, 5)`
gives `y` with `bisect_right` and `x` with `bisect_left`; every other query agrees.

That is what makes the bug durable: it is right on every version *between*
writes, and a hand-made test picking "some old version" usually picks one.
:::

:::check
A colleague implements `delete(key)` as `del vers[key]; del vals[key]`, arguing
that the key is gone so its history is useless. Where are they wrong?
--
They have confused the current state with the whole history. Deleting the lists
destroys every past version of that key, so a query aimed *before* the delete —
which must still answer correctly — returns `NULL`, or worse, values from a later
re-creation. The structure stops being persistent for that key, which is the one
property it exists to provide.

The right move is to append a tombstone: a stamped entry carrying a reserved
value that cannot collide with a real one. Then the predecessor search lands on
the tombstone for versions after the delete and on the real value for versions
before it, and both answers come out of the same code path with no branch.

After a tombstone, a later `put` appends normally and the history reads
`value, tombstone, value` — a full account of the key's life. Deleting and
recreating the lists throws that ordering evidence away.
:::

:::check
*Versioned Key-Value Store with Suffix Truncation* has `PUT key version value`
with a caller-supplied version, and `DELETE key version` that removes every
stored version `>= version`. Which parts of the proof survive, and what changes
in the implementation?
--
Invariant (I3) — "the answer is the value of the entry with the greatest stamp
`<= v`" — survives untouched, because it is a statement about whatever is
currently stored, and both operations leave the list sorted. The query code does
not change at all.

What breaks is the *append* step of (I1) and the argument that old queries are
unaffected. Stamps no longer arrive in order, so a `PUT` must be an ordered
insertion (`bisect` the position, then `insert`, or overwrite when that exact
version exists), and inserting in the middle genuinely changes what earlier
queries see. That is intended: this is not a partially persistent store, it is a
mutable map indexed by version.

`DELETE` is a suffix truncation: `bisect_left` for the first stamp `>= version`,
then cut the tail. It is the one operation here that reclaims memory, possible
only because the problem permits history to be destroyed — which is also the tell
that this is a sorted-list problem wearing versioning vocabulary.
:::

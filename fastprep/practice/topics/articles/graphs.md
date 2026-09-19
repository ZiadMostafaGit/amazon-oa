# Graphs: Representation

> A graph is not a picture and not a list of edges. It is a function from a
> vertex to its neighbours, and the way you choose to store that function fixes
> the cost of every algorithm you will ever run on top of it.

## When you reach for it

You reach for a graph the moment a problem gives you a set of things and a set
of pairwise relations between them, and then asks a question that depends on
*chains* of those relations rather than on the relations one at a time.

"Is there a road from city 4 to city 9" is a chain question. "How many roads
leave city 4" is not — a counter answers that. The tell is that the answer to
the question about `u` and `v` can change when you add an edge that touches
neither of them. That is what makes you build a structure instead of scanning
the input.

This is the twelfth most used topic in this collection: 383 problems here rest
on it. They arrive in a handful of disguises.

- **The edge list, plainly.** *Count Connected Components*, *Number of Connected
  Components in an Undirected Graph*, *Minimum Edges to Connect All Components*
  — `n` and a list of pairs, nothing more.
- **A matrix instead.** *Shortest Distances From an Adjacency Matrix* hands you
  the `n × n` grid and expects you to read it as a graph.
- **Labels instead of indices.** *Most Active Caller by Distinct Contacts*,
  *Initial and Final Accounts in a Transfer Chain*, *Directly Linked Users* give
  names or account ids, so the first thing you build is not the graph but the
  dictionary turning a label into an integer.
- **No edges at all.** *Count Prefix Paths in a Character Graph* and *Minimum
  Clicks Between Wiki Pages* describe a graph whose neighbours you compute on
  demand. Nothing is ever stored.
- **Direction that matters.** *Directed Path Existence*, *Detect a Cycle in a
  Directed Graph*, *Find the Root of a Directed Tree* — read the same input
  symmetrically and you get a confident wrong answer.

This chapter is about that layer alone: turning a statement into a structure you
can traverse, and knowing what the choice costs. The traversals themselves are
[[bfs]] and [[dfs]]; the art of inventing vertices that the statement never
mentions is [[graph-modelling]].

Two shapes look like graphs and are not. The first counts graphs rather than
traversing one: *Drawing Edge* asks how many simple undirected graphs exist on
`n` labelled vertices with `n` up to `10^9`, and there is nothing to build — see
"What it costs". The second asks only about grouping, with no distances and no
directions; [[union-find]] answers that without an adjacency list existing
anywhere.

## The idea

Store, for each vertex, the list of vertices it points at. Everything else is a
storage decision about that one idea.

Write `N(u)` for the neighbours of `u`. An algorithm on a graph only ever does
two things: it asks for `N(u)`, and it asks whether `v` is in `N(u)`. A
representation is a choice about which of those two you make cheap.

- **Adjacency list** — an array of `n` lists. `N(u)` is handed to you in
  `O(deg u)`; membership costs a scan.
- **Adjacency matrix** — an `n × n` grid of bits. Membership is one lookup;
  `N(u)` costs a full row of `n` cells whether the vertex has a thousand
  neighbours or none.
- **Edge list** — the input, unprocessed. Neither operation is cheap, but
  algorithms that only ever sweep over all edges ([[minimum-spanning-tree]],
  [[bellman-ford]]) never need anything better.
- **Implicit** — a function that computes `N(u)` when asked. Zero memory, and
  the only option when the vertex set is astronomically large.

<svg viewBox="0 0 680 270" role="img" aria-label="a five-vertex graph drawn on the left and the same graph as five rows of an adjacency list on the right">
  <g>
    <circle cx="70" cy="60" r="18"/>
    <text x="70" y="66" text-anchor="middle">0</text>
    <circle cx="180" cy="60" r="18"/>
    <text x="180" y="66" text-anchor="middle">1</text>
    <circle cx="125" cy="150" r="18"/>
    <text x="125" y="156" text-anchor="middle">3</text>
    <circle cx="60" cy="220" r="18"/>
    <text x="60" y="226" text-anchor="middle">2</text>
    <circle cx="170" cy="220" r="18"/>
    <text x="170" y="226" text-anchor="middle">4</text>
    <line x1="88" y1="60" x2="162" y2="60"/>
    <line x1="80" y1="76" x2="115" y2="133"/>
    <line x1="170" y1="76" x2="135" y2="133"/>
    <line x1="78" y1="220" x2="152" y2="220"/>
    <text x="120" y="255" text-anchor="middle">four undirected edges</text>
    <text x="300" y="52">0:</text>
    <rect class="fill" x="330" y="32" width="42" height="26" rx="4"/>
    <text x="351" y="52" text-anchor="middle">1</text>
    <rect class="fill" x="378" y="32" width="42" height="26" rx="4"/>
    <text x="399" y="52" text-anchor="middle">3</text>
    <text x="300" y="90">1:</text>
    <rect class="fill" x="330" y="70" width="42" height="26" rx="4"/>
    <text x="351" y="90" text-anchor="middle">0</text>
    <rect class="fill" x="378" y="70" width="42" height="26" rx="4"/>
    <text x="399" y="90" text-anchor="middle">3</text>
    <text x="300" y="128">2:</text>
    <rect class="fill" x="330" y="108" width="42" height="26" rx="4"/>
    <text x="351" y="128" text-anchor="middle">4</text>
    <text x="300" y="166">3:</text>
    <rect class="fill" x="330" y="146" width="42" height="26" rx="4"/>
    <text x="351" y="166" text-anchor="middle">0</text>
    <rect class="fill" x="378" y="146" width="42" height="26" rx="4"/>
    <text x="399" y="166" text-anchor="middle">1</text>
    <text x="300" y="204">4:</text>
    <rect class="fill" x="330" y="184" width="42" height="26" rx="4"/>
    <text x="351" y="204" text-anchor="middle">2</text>
    <text x="300" y="245">8 stored entries for 4 edges</text>
  </g>
</svg>

Two things about that picture are worth saying out loud, because both become
bugs later.

**An undirected edge is stored twice.** The structure only knows about one-way
links; symmetry is something you impose when you build, by pushing `v` into
`N(u)` *and* `u` into `N(v)`. Nothing later will remind you.

**The order inside a row is your insertion order, not a property of the graph.**
Two correct builds can produce different rows, so a depth-first search visits the
vertices in a different order and prints a different — still correct — answer.
*Deterministic Depth-First Graph Traversal* exists because of this: when one
specific ordering is expected, neighbour order is part of the specification and
you must sort.

## Worked by hand

Take the graph above: `n = 5`, and the edges given in this order,
`(0,1), (0,3), (1,3), (2,4)`, undirected. Build the adjacency list by pushing
each edge in both directions.

| step | edge | `adj[0]` | `adj[1]` | `adj[2]` | `adj[3]` | `adj[4]` |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | — | `[]` | `[]` | `[]` | `[]` | `[]` |
| 1 | (0,1) | `[1]` | `[0]` | `[]` | `[]` | `[]` |
| 2 | (0,3) | `[1,3]` | `[0]` | `[]` | `[0]` | `[]` |
| 3 | (1,3) | `[1,3]` | `[0,3]` | `[]` | `[0,1]` | `[]` |
| 4 | (2,4) | `[1,3]` | `[0,3]` | `[4]` | `[0,1]` | `[2]` |

Eight entries for four edges. That is not a coincidence and it is the single
most useful fact in this chapter; it gets a proof below.

Now build the same graph the way a fast judge solution does: flat arrays, no
per-vertex list objects. This is the **compressed sparse row** layout — one
array `head` holding every neighbour of every vertex back to back, and one array
`start` saying where each vertex's stretch begins. It is a [[counting-sort]] of
the half-edges by their tail.

Expand the four edges into eight directed half-edges, forward ones first:
`0→1, 0→3, 1→3, 2→4, 1→0, 3→0, 3→1, 4→2`. Count tails: `deg = [2,2,1,2,1]`.
Prefix-sum them: `start = [0,2,4,5,7,8]`. Set a cursor per vertex,
`cur = [0,2,4,5,7]`, and scatter.

| # | half-edge | `cur[u]` | writes | `cur` after |
| --- | --- | --- | --- | --- |
| 1 | 0→1 | 0 | `head[0] = 1` | `[1,2,4,5,7]` |
| 2 | 0→3 | 1 | `head[1] = 3` | `[2,2,4,5,7]` |
| 3 | 1→3 | 2 | `head[2] = 3` | `[2,3,4,5,7]` |
| 4 | 2→4 | 4 | `head[4] = 4` | `[2,3,5,5,7]` |
| 5 | 1→0 | 3 | `head[3] = 0` | `[2,4,5,5,7]` |
| 6 | 3→0 | 5 | `head[5] = 0` | `[2,4,5,6,7]` |
| 7 | 3→1 | 6 | `head[6] = 1` | `[2,4,5,7,7]` |
| 8 | 4→2 | 7 | `head[7] = 2` | `[2,4,5,7,8]` |

Result: `head = [1,3,3,0,4,0,1,2]`, and vertex `v`'s neighbours are
`head[start[v] : start[v+1]]`.

<svg viewBox="0 0 620 195" role="img" aria-label="the head array of eight cells divided into five buckets by the start array">
  <g>
    <rect class="fill" x="40" y="70" width="60" height="40" rx="3"/>
    <text x="70" y="96" text-anchor="middle">1</text>
    <rect class="fill" x="100" y="70" width="60" height="40" rx="3"/>
    <text x="130" y="96" text-anchor="middle">3</text>
    <rect x="160" y="70" width="60" height="40" rx="3"/>
    <text x="190" y="96" text-anchor="middle">3</text>
    <rect x="220" y="70" width="60" height="40" rx="3"/>
    <text x="250" y="96" text-anchor="middle">0</text>
    <rect class="fill" x="280" y="70" width="60" height="40" rx="3"/>
    <text x="310" y="96" text-anchor="middle">4</text>
    <rect x="340" y="70" width="60" height="40" rx="3"/>
    <text x="370" y="96" text-anchor="middle">0</text>
    <rect x="400" y="70" width="60" height="40" rx="3"/>
    <text x="430" y="96" text-anchor="middle">1</text>
    <rect class="fill" x="460" y="70" width="60" height="40" rx="3"/>
    <text x="490" y="96" text-anchor="middle">2</text>
    <text x="70" y="58" text-anchor="middle">v0</text>
    <text x="190" y="58" text-anchor="middle">v1</text>
    <text x="310" y="58" text-anchor="middle">v2</text>
    <text x="430" y="58" text-anchor="middle">v3</text>
    <text x="490" y="58" text-anchor="middle">v4</text>
    <line x1="40" y1="62" x2="40" y2="125"/>
    <line x1="160" y1="62" x2="160" y2="125"/>
    <line x1="280" y1="62" x2="280" y2="125"/>
    <line x1="340" y1="62" x2="340" y2="125"/>
    <line x1="460" y1="62" x2="460" y2="125"/>
    <line x1="520" y1="62" x2="520" y2="125"/>
    <text x="40" y="142" text-anchor="middle">0</text>
    <text x="160" y="142" text-anchor="middle">2</text>
    <text x="280" y="142" text-anchor="middle">4</text>
    <text x="340" y="142" text-anchor="middle">5</text>
    <text x="460" y="142" text-anchor="middle">7</text>
    <text x="520" y="142" text-anchor="middle">8</text>
    <text x="40" y="175">start: one prefix sum of the degrees, and the rows never move</text>
  </g>
</svg>

Three things the trace shows that the finished code would not.

**The rows come out in a different order.** The list build gave `adj[1] = [0,3]`;
the CSR build gave `head[2:4] = [3,0]`, because the forward half-edge `1→3` was
scattered before the backward half-edge `1→0`. Both are the same graph. If your
answer depends on which came first, you have a specification to read again, not
a bug to hunt.

**No cursor ever crossed into the next bucket.** `cur[0]` stopped at 2, exactly
`start[1]`; `cur[3]` stopped at 7, exactly `start[4]`. That is the whole
correctness question for this build, and it holds because the boundaries were
computed from the same counts that the scatter later consumes. Break that
agreement — count one set of edges and scatter a slightly different set — and a
neighbour lands quietly under the wrong vertex.

**The degrees sum to 8.** Five vertices, four edges, eight entries. Not
`n × max degree = 10`, and not `n²= 25`. That gap is why traversals are linear.

## Why it is correct

There is no algorithm here to be correct or incorrect about — there is a data
structure, so the thing to prove is that it represents what we claim. Two
statements: the counting law the costs depend on, and the invariant of the
bucket build.

:::proof The bucket build stores exactly the right neighbours
**Setup.** Vertices are `0 … n-1`. Fix a sequence of *half-edges*
`H = h₁ … h_M`, each a pair `(uₖ, vₖ)` read as "`uₖ` points at `vₖ`". For an
undirected input we emit two half-edges per edge, `(u,v)` and `(v,u)`; for a
directed input, one. Let `deg[u] = |{k : uₖ = u}|`, let `start[0] = 0` and
`start[v+1] = start[v] + deg[v]`, let `cur` start as a copy of `start[0..n-1]`,
and let `head` have length `M`.

**Lemma (the buckets tile the array).** Every half-edge has exactly one tail, so
`Σ_v deg[v] = M`, and the telescoping sum gives `start[n] = M`. Since every
`deg[v] >= 0`, `start` is non-decreasing, so the intervals
`B_v = [start[v], start[v+1])` are pairwise disjoint and their union is
`[0, M)`.

**Invariant.** After the first `k` half-edges have been scattered, writing
`c_k(v) = |{j <= k : u_j = v}|`:

- **(I1)** `cur[v] = start[v] + c_k(v)` for every `v`;
- **(I2)** the cells `head[start[v] … cur[v]-1]` hold, in order, the heads `v_j`
  of exactly those `j <= k` with `u_j = v`;
- **(I3)** no cell outside `⋃_v [start[v], cur[v])` has been written.

**Base case.** `k = 0`: every `c_0(v) = 0`, so `cur = start` and each range in
(I2) is empty, which is what has been written — nothing. All three hold.

**Inductive step.** Suppose the invariant holds after `k < M` and the next
half-edge is `h_{k+1} = (u, v)`. Because `h_{k+1}` itself has tail `u` and is not
counted in `c_k(u)`, we have `c_k(u) <= deg[u] - 1`, so by (I1)

    cur[u] = start[u] + c_k(u) <= start[u] + deg[u] - 1 = start[u+1] - 1.

So `cur[u] ∈ B_u`: the write lands strictly inside `u`'s own bucket. By the
Lemma that cell belongs to no other bucket, so for every `w ≠ u` the range in
(I2) is untouched and its claim survives verbatim; (I3) survives because the
written cell is `cur[u]`, which is inside `[start[u], cur[u]]`. For `u` itself,
the cell written is the one immediately after its current stored range, so the
range grows by one cell holding `v` at its end — which is exactly the list of
heads for `j <= k+1` with `u_j = u`, in order. Incrementing `cur[u]` re-establishes
(I1) since `c_{k+1}(u) = c_k(u) + 1`, and `c_{k+1}(w) = c_k(w)` elsewhere.

**Termination.** The loop runs `M` times and each iteration does O(1) work, so it
stops. At `k = M`, `c_M(v) = deg[v]`, hence `cur[v] = start[v] + deg[v] =
start[v+1]`, and (I2) reads: `head[start[v] … start[v+1]-1]` is exactly the
multiset of heads of the half-edges with tail `v`, in input order. By the Lemma
those ranges tile `[0, M)`, so every cell was written exactly once and none is
stale. That is precisely the adjacency structure we claimed. ∎

**Corollary (the handshake lemma).** For an undirected graph with `m` edges,
`M = 2m`, so `Σ_v deg(v) = 2m`. For a directed graph, `M = m` and
`Σ_v outdeg(v) = Σ_v indeg(v) = m`.
:::

Now the assumptions, because that is where the bugs live.

- **Vertices are dense integers `0 … n-1`,** and `n` is given, not inferred. The
  Lemma sizes `start` from `n`; if you deduce the vertex set from the edges you
  will build a smaller graph. *Count Connected Components* and *Minimum Edges to
  Connect All Components* both include isolated vertices in the answer, so this
  is not a technicality — it is the difference between right and wrong. Labelled
  inputs like *Directly Linked Users* must be interned through a dictionary
  first, and the dictionary must be seeded from the vertex list, not from the
  edges.
- **The counting pass and the scatter pass see the same multiset of half-edges,
  in the same way.** The step used `c_k(u) <= deg[u] - 1`, which is only true if
  `deg` counted this very half-edge. Filter self-loops out of one pass and not
  the other and a cursor walks into the next vertex's bucket — no exception, no
  index error, just a neighbour appearing under the wrong vertex.
- **Multiset, not set.** Nothing deduplicates. A repeated pair produces a
  repeated entry, which is correct for traversal and wrong for counting: *Most
  Active Caller by Distinct Contacts* asks for *distinct* contacts, so the
  deduplication has to be yours and explicit.
- **Symmetry is imposed, not discovered.** The proof never mentions undirected
  graphs except at the point where we choose to emit two half-edges. Emit one and
  you have built a perfectly valid directed graph that answers a different
  question.
- **A self-loop in an undirected graph emits two half-edges,** both `u→u`, so it
  adds 2 to `deg(u)`. That convention is exactly what keeps `Σ deg = 2m` true,
  and it is why degree-based arguments do not need a special case for loops.
- **Order within a row is the input order and nothing more.** No claim is made,
  none may be relied on.

## What it costs

Every cost in this chapter follows from the handshake lemma, so derive them
rather than remembering them.

**Building.** The counting pass touches each of the `M` half-edges once, the
prefix sum runs over `n` vertices, the scatter touches each half-edge once:
`Θ(n + M)`, which is `Θ(n + m)` directed and `Θ(n + 2m) = Θ(n + m)` undirected.
The list-of-lists build is the same `Θ(n + m)` with a larger constant, since each
`append` may resize.

**Traversing everything.** A traversal visits each vertex once and walks its row:

    Σ_v (1 + deg v) = n + Σ_v deg v = n + 2m.

That is the entire reason [[bfs]] and [[dfs]] are `Θ(V + E)`. Notice what the
sum did *not* do: it did not become `n × max deg`. High-degree vertices are paid
for once each, not once per vertex. On the constraint line of *Minimum Edges to
Connect All Components* — `n <= 10^5`, `m <= 2 × 10^5` — a full traversal is
about `5 × 10^5` steps.

**The matrix, for contrast.** Row `u` has `n` cells whatever `deg(u)` is, so the
same traversal costs `Σ_v n = n²`. With the numbers above that is `10^10` steps
and `10^10` cells of memory: not slow, impossible. Setting the two costs equal,
`n + 2m ≈ n²`, gives the crossover at `m ≈ n²/2`: the matrix only pays on a dense
graph, and only up to a few thousand vertices. That is why *Shortest Distances
From an Adjacency Matrix* can hand you one, and why [[floyd-warshall]] — `Θ(n³)`
anyway — uses one without apology.

**Space.** CSR: `n + 1` integers for `start` plus `2m` for `head`. List of lists:
the same `2m` entries plus `n` list objects with their headers — in CPython an
empty list is 56 bytes before it holds anything, so a million vertices costs
about 56 MB before a single edge. A dict of lists adds a hash table on top. This
is the usual reason an asymptotically fine solution dies on memory.

**Asking "is `u` adjacent to `v`".** The matrix answers in one lookup. An
adjacency list must scan, at `O(deg u)`. Average degree is `2m/n`, so `k` such
tests cost `O(k·m/n)` — harmless once, quadratic inside a loop over pairs. If a
problem really needs repeated adjacency tests on a sparse graph, store a `set`
per vertex as well and pay one hash per test ([[hash-tables]]); do not scan.

**The cost people forget** is the translation layer. Interning string labels
costs a dictionary lookup per endpoint — expected O(1), but a string's hash is
proportional to its length, and on *Initial and Final Accounts in a Transfer
Chain* the labels, not the graph, dominate. The other is sorting rows for
determinism: `Σ_v deg(v) log deg(v) <= 2m log n`, cheap, but a `log` you added.

**And the counting question.** *Drawing Edge* wants the number of simple
undirected graphs on `n` labelled vertices — the same counting read backwards.
The edge slots are the unordered pairs, `C(n,2) = n(n-1)/2` of them, each
independently present or absent, so there are `2^(n(n-1)/2)` graphs. With `n` up
to `10^9` the exponent is about `5 × 10^17`: compute
`pow(2, n*(n-1)//2, 10**9+7)`, some 60 squarings ([[fast-exponentiation]]), or
reduce the exponent mod `p-1` by Fermat ([[modular-arithmetic]]). The word
"edge" is not a licence to allocate.

## The implementation

```python run
from collections import deque


def adjacency_list(n, edges, directed=False):
    adj = [[] for _ in range(n)]              # never [[]] * n
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj


def csr(n, edges, directed=False):
    """The same graph in two flat arrays: no per-vertex list objects."""
    half = list(edges) + ([] if directed else [(v, u) for u, v in edges])
    deg = [0] * n
    for u, _ in half:
        deg[u] += 1                            # pass 1: count the tails
    start = [0] * (n + 1)
    for v in range(n):
        start[v + 1] = start[v] + deg[v]       # prefix sums are the boundaries
    cur, head = start[:n], [-1] * len(half)
    for u, v in half:
        head[cur[u]] = v                       # pass 2: scatter
        cur[u] += 1
    assert cur == start[1:], "every bucket filled exactly to its boundary"
    return start, head


def bfs(src, neighbours, n):
    dist = [-1] * n
    dist[src], q = 0, deque([src])
    while q:
        u = q.popleft()
        for w in neighbours(u):
            if dist[w] < 0:
                dist[w] = dist[u] + 1
                q.append(w)
    return dist


n, edges = 5, [(0, 1), (0, 3), (1, 3), (2, 4)]
adj = adjacency_list(n, edges)
start, head = csr(n, edges)
print("adjacency list :", adj)
print("start          :", start)
print("head           :", head)

for v in range(n):
    assert sorted(head[start[v]:start[v + 1]]) == sorted(adj[v]), v
print("row of vertex 1: list", adj[1], "vs CSR", head[start[1]:start[2]],
      "- same set, different order")

deg = [len(a) for a in adj]
print("degrees        :", deg, "sum", sum(deg), "= 2 * |E| =", 2 * len(edges))
assert sum(deg) == 2 * len(edges) == len(head)

touched = sum(1 for u in range(n) for _ in adj[u])
print("slots a full scan touches:", touched, "(= 2|E|, not n * max degree)")
assert touched == 2 * len(edges)

d_list = bfs(0, lambda u: adj[u], n)
d_csr = bfs(0, lambda u: head[start[u]:start[u + 1]], n)
print("BFS from 0     :", d_list, "(-1 means unreachable)")
assert d_list == d_csr == [0, 1, -1, 1, -1]
print("two representations, one answer")
```

Four lines are doing the real work.

`adj = [[] for _ in range(n)]` builds `n` distinct lists. The comment is there
because `[[]] * n` builds one list and `n` references to it, and the resulting
bug is demonstrated under "Traps".

`if not directed: adj[v].append(u)` is the only place in the program that knows
the graph is undirected. Put the decision in the builder and it is made once; put
it at the call sites and it will eventually be forgotten at one of them.

`start[v + 1] = start[v] + deg[v]` is the prefix sum from the proof. `start` has
`n + 1` entries on purpose: the extra slot means `head[start[v] : start[v+1]]`
works for the last vertex with no special case, exactly as with [[prefix-sums]].

`assert cur == start[1:]` is the invariant from the proof, written as an
executable claim. Every cursor must finish precisely at its bucket's upper bound.
If the two passes ever disagree about which edges exist, this assertion fires at
build time instead of producing a graph that is subtly not yours.

`bfs` takes a `neighbours` *function*, so the one routine runs over a list of
lists, over CSR slices, and — in the next block — over a grid with no stored
edges at all. That signature is the chapter's idea made practical.

## Variants you will meet

**List of lists.** The default. `n` known, vertices `0 … n-1`.

**Dict of lists.** Vertices are labels, or the numbering is sparse. Costs a hash
per access; convenient, and slower than it looks in a hot loop. *Most Active
Caller by Distinct Contacts* and *Directly Linked Users* arrive this way.

**Intern, then use a list.** Map labels to `0 … n-1` once, solve on arrays, map
back at the end. Usually right when the graph is large.

**CSR / flat arrays.** As above: no per-vertex objects, best cache behaviour.
Worth it when `m` is in the millions.

**Adjacency matrix.** `n²` cells, O(1) edge test, `Θ(n²)` scan. The input format
for *Shortest Distances From an Adjacency Matrix*, and the natural home of
[[floyd-warshall]]. A bitset row makes it `n²/64` words, which is how dense
reachability is done.

**Edge list, kept as given.** [[minimum-spanning-tree]] sorts it; [[bellman-ford]]
sweeps it `n-1` times; neither ever asks for `N(u)`.

**Weighted.** Store pairs: `adj[u].append((v, w))`. Resist a separate
`weight[(u,v)]` dictionary — it costs a hash per relaxation and cannot represent
two edges between one pair. This is what [[dijkstra]] wants, and *Dijkstra
Shortest Paths in a Weighted Undirected Graph* is where you will want it.

**The transpose.** Reverse every edge, or build indegrees alongside outdegrees.
*Find the Root of a Directed Tree* is "the unique vertex with indegree 0", which
is a degree array and no traversal at all. [[topological-sort]] runs on
indegrees, and [[strongly-connected]] needs the whole reversed graph.

**Implicit graphs.** `N(u)` is a generator. Grids ([[grid-bfs]],
[[matrix-traversal]]), states of a puzzle, strings one edit apart. *Count Prefix
Paths in a Character Graph* and *Minimum Clicks Between Wiki Pages* are of this
family: the vertex set is defined by a rule, and materialising it is the mistake.
[[graph-modelling]] is the chapter on inventing these.

**Trees as graphs.** Children lists (*Maximum Depth of an N-ary Tree*) or a
parent array are already graphs; a tree given as `n-1` undirected edges needs a
root chosen and a parent tracked so you do not walk back up. See [[trees]].

**Two-mode inputs.** When `k` people share a group, an edge between every pair
costs `O(k²)`. Add one vertex for the group and `k` edges instead: a
representation change that turns a quadratic build linear, and the core trick of
[[graph-modelling]].

```python run
def matrix(n, edges, directed=False):
    m = [[0] * n for _ in range(n)]
    for u, v in edges:
        m[u][v] = 1                          # assignment, so a repeat is lost
        if not directed:
            m[v][u] = 1
    return m


def lists(n, edges, directed=False):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj


# 1. a multigraph: the pair (0, 1) is given twice
n, edges = 3, [(0, 1), (0, 1), (1, 2)]
adj, mat = lists(n, edges), matrix(n, edges)
print("adjacency list of 0 :", adj[0], "-> degree", len(adj[0]))
print("matrix row of 0     :", mat[0], "-> row sum", sum(mat[0]))
assert len(adj[0]) == 2 and sum(mat[0]) == 1
print("the matrix merged the parallel edge; the list kept both")
print("distinct neighbours of 0 :", sorted(set(adj[0])))

# 2. what each representation costs to scan, on a sparse graph
N = 300
ring = [(i, (i + 1) % N) for i in range(N)]       # N vertices, N edges
adj, mat = lists(N, ring), matrix(N, ring)
list_steps = sum(len(adj[u]) for u in range(N))
mat_steps = N * N
print("ring on %d vertices: list scan %d steps, matrix scan %d, ratio %d"
      % (N, list_steps, mat_steps, mat_steps // list_steps))
assert list_steps == 2 * N and mat_steps == N * N
print("matrix cells that are 1:", sum(sum(r) for r in mat), "of", N * N,
      "- %.2f%% useful" % (100.0 * 2 * N / (N * N)))

# 3. an implicit graph: neighbours computed, never stored
ROWS, COLS = 3, 4
blocked = {(1, 1), (1, 2)}


def grid_neighbours(cell):
    r, c = cell
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and (nr, nc) not in blocked:
            yield (nr, nc)


seen, stack = {(0, 0)}, [(0, 0)]
while stack:
    for nxt in grid_neighbours(stack.pop()):
        if nxt not in seen:
            seen.add(nxt)
            stack.append(nxt)
print("grid cells reachable from (0,0):", len(seen), "of",
      ROWS * COLS - len(blocked), "open cells - zero edges stored")
assert len(seen) == ROWS * COLS - len(blocked)
```

## Recognising it in a statement

Ordered by how much you should trust them.

1. **`edges[i] = [u, v]` with `n` given separately.** A giveaway — and `n` being
   separate is itself the hint that isolated vertices exist and count.
2. **"n cities / nodes / users numbered 0 through n-1"** followed by pairs. List
   of lists; stop thinking about representation.
3. **"bidirectional", "mutual", "both ways"** — undirected, push twice. Its
   absence is information: *Directed Path Existence* and *Detect a Cycle in a
   Directed Graph* mean what they say.
4. **An `n × n` grid of 0/1 or of distances,** with `n` in the hundreds. The
   matrix *is* the input; index it, do not convert it. Symmetric means
   undirected.
5. **Constraint arithmetic.** `n <= 10^5` with `m <= 2 × 10^5` says sparse, so
   adjacency list; `n <= 400` with an all-pairs question says dense, so matrix
   and probably [[floyd-warshall]]. The constraint line picks the representation
   before you have read the question.
6. **Labels, names, emails, account ids** as vertices — intern them; the hash map
   is half the solution and all of the off-by-one risk.
7. **A described relation with no edge array at all** — "two words are joined if
   they differ in one letter". Implicit graph; write the neighbour function.

Anti-signals, which matter as much:

- **`n` up to `10^9` and the word "edge".** You are being asked to *count*, not
  to build. *Drawing Edge* is the example: the answer is `2^(n(n-1)/2)` mod a
  prime, pure [[combinatorics]].
- **Only grouping is ever asked.** No distances, no order, no direction — merges
  and questions about blobs. [[union-find]] is smaller and faster.
- **The relation is over a numeric range you can sort.** "Pairs within distance
  `k`" is often [[sorting]] plus [[two-pointers]]; materialising the `O(n²)` edge
  set to traverse it is the trap.
- **Every pair is related.** A complete graph has no structure to exploit.

## Traps

**`adj = [[]] * n`.** All `n` rows are the same list object, so every vertex
appears adjacent to every edge endpoint in the input. Symptom: the graph looks
wildly over-connected, component counts collapse toward 1, and the program never
raises. Demonstrated below.

**Pushing an undirected edge once.** Symptom: reachability is correct from some
sources and wrong from others — the bug hides on any test where the search
happens to start at the right end. Demonstrated below.

**Inferring the vertex set from the edges.** Symptom: every count is short by the
number of isolated vertices, and the samples pass because samples rarely have
any. *Count Connected Components* punishes this specifically. Demonstrated below.

**1-indexed input into a 0-indexed array.** Either allocate `n + 1` and ignore
row 0, or subtract 1 where you read the edge — doing both, or neither, is the
usual outcome. Symptom: an `IndexError` if you are lucky, one phantom isolated
vertex if you are not.

**Self-loops and parallel edges.** A self-loop is harmless to a visited-set
traversal and fatal to degree arithmetic that assumes simplicity; parallel edges
make `len(adj[u])` a count of edges, not of distinct neighbours. When the
constraints do not promise a simple graph, decide explicitly.

**Relying on neighbour order.** Symptom: correct answers in the wrong order.
*Deterministic Depth-First Graph Traversal* wants a specific traversal sequence,
so sort each row once after building, and say in a comment that you did.

**Membership tests inside a loop.** `if v in adj[u]` is `O(deg u)`; nested in a
loop over vertices it is quadratic. Keep a set, or a matrix, if you need the
test. And never append to `adj[u]` while looping over it.

**Recursion depth.** A path graph on `10^5` vertices will overflow a recursive
DFS long before it is slow. Write the iterative form ([[dfs]]).

```python run
def components(n, adj):
    seen, count = [False] * n, 0
    for s in range(n):
        if not seen[s]:
            count += 1
            seen[s], stack = True, [s]
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if not seen[v]:
                        seen[v] = True
                        stack.append(v)
    return count


def reachable(adj, s, t):
    seen, stack = {s}, [s]
    while stack:
        u = stack.pop()
        if u == t:
            return True
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return False


n, edges = 5, [(0, 1), (2, 3)]     # truth: {0,1}, {2,3}, {4} -> 3 components

right = [[] for _ in range(n)]
for u, v in edges:
    right[u].append(v)
    right[v].append(u)

aliased = [[]] * n                  # bug 1: five names for ONE list
for u, v in edges:
    aliased[u].append(v)
    aliased[v].append(u)

one_way = [[] for _ in range(n)]    # bug 2: an undirected edge stored once
for u, v in edges:
    one_way[u].append(v)

labels = sorted({x for e in edges for x in e})          # bug 3: n taken from edges
idx = {x: i for i, x in enumerate(labels)}
inferred = [[] for _ in labels]
for u, v in edges:
    inferred[idx[u]].append(idx[v])
    inferred[idx[v]].append(idx[u])

print("correct           ", right, "-> components", components(n, right))
print("[[]] * n          ", aliased, "-> components", components(n, aliased))
print("  same object?    ", aliased[0] is aliased[4], " correct:", right[0] is right[4])
print("one direction only", one_way, "-> reachable(1 -> 0)", reachable(one_way, 1, 0),
      " correct:", reachable(right, 1, 0))
print("n taken from edges", inferred, "-> components", components(len(labels), inferred))

assert components(n, right) == 3
assert components(n, aliased) == 2          # every vertex shares one neighbour list
assert reachable(right, 1, 0) and not reachable(one_way, 1, 0)
assert components(len(labels), inferred) == 2   # vertex 4 never existed
print()
print("three bugs, three different wrong answers, no exception from any of them")
```

The third deserves a second look. `inferred` is a perfectly good adjacency list
of a perfectly good graph — just not the one you were given. No assertion inside
the build catches it, because the build is correct; only `len(adj) == n` does,
and only if you wrote `n` down when you read the statement.

## What to memorise

Four lines, one sentence, one habit.

**The template**, which should need no thought:

```python
adj = [[] for _ in range(n)]          # n from the STATEMENT, not from the edges
for u, v in edges:
    adj[u].append(v)
    adj[v].append(u)                  # delete this line if directed
```

**The sentence** that turns a statement into it: *"What are my vertices, what is
`n`, is the relation symmetric, is it weighted, and are my labels already
integers?"* Five answers, written down before any code. Every trap in this
chapter is one of those five answered wrongly.

**The habit**: build the graph in a function that takes `n` and returns the
structure; never inline the build into the solver. A builder has one place for
the `directed` flag, one for the indexing convention, and one to sort the rows
when determinism is required.

Numbers worth carrying: `Σ deg(v) = 2m` for undirected, `Σ outdeg(v) = m` for
directed; adjacency list space is `n + 2m`, matrix space is `n²`; a traversal is
`Θ(n + m)` on a list and `Θ(n²)` on a matrix; the matrix is affordable to about
a few thousand vertices; a graph on `n` vertices has `C(n,2) = n(n-1)/2` possible
undirected edges, hence `2^(n(n-1)/2)` distinct simple graphs; connecting `c`
components takes exactly `c - 1` edges.

## Check yourself

:::check
Why is a full traversal of an adjacency list `Θ(V + E)` rather than
`Θ(V × max degree)`? Both bound the same loop.
--
Because the inner loop over `adj[u]` runs `deg(u)` times, not `max deg` times,
and the total is the *sum* of the degrees, not `n` copies of the largest one:

    Σ_v (1 + deg v) = n + Σ_v deg v = n + 2m

by the handshake lemma. `Θ(V × max deg)` is a valid upper bound and a bad one: a
star graph on `10^5` vertices has `max deg = 10^5 - 1`, so that bound reads
`10^10` while the truth is about `2 × 10^5`.

The deeper point is that the two bounds differ because degree is not distributed
evenly, and the summation is what notices. Any time you bound a graph loop by
multiplying instead of summing, you are probably throwing away the algorithm.
:::

:::check
Someone says: "use an adjacency matrix — checking whether an edge exists is O(1)
instead of O(degree), so it is strictly better." Where are they wrong?
--
They have optimised the operation the algorithm does not perform. BFS, DFS,
topological sort, Dijkstra and connected components never ask "is `u` adjacent to
`v`"; they ask "give me all neighbours of `u`". The matrix answers *that* in
`Θ(n)` per vertex regardless of degree, so a traversal becomes `Θ(n²)` where the
list gives `Θ(n + m)`. The memory is worse than the time: at `n = 10^5` the
matrix is `10^10` cells, and the machine refuses before the clock matters.

The correct version of their point: when adjacency *tests* really do dominate — a
triangle count on a dense graph, or [[floyd-warshall]] — a matrix or a bitset row
is right, which is why *Shortest Distances From an Adjacency Matrix* hands you
one. The choice follows the operation mix, not one operation's headline cost.
:::

:::check
The CSR build counts degrees in one pass and scatters in a second. Suppose the
counting pass skips self-loops (`if u != v: deg[u] += 1`) but the scatter pass
does not. What exactly goes wrong, and why is there no crash?
--
The proof's inductive step needed `c_k(u) <= deg[u] - 1` to conclude
`cur[u] < start[u+1]`. With a self-loop uncounted, `deg[u]` is one short of the
number of half-edges with tail `u`, so the last of them writes at
`cur[u] = start[u+1]` — the first cell of the *next* non-empty bucket.

There is no crash because `head` was allocated with one cell per half-edge
actually scattered, while the buckets only cover `start[n] = M - (number of
skipped loops)` of them. The overflowing writes therefore land at indices that
exist, and Python is happy to overwrite a cell. The symptom is a neighbour of `u`
appearing in the row of a later vertex, and one of that vertex's real neighbours
being lost — a graph that is wrong in a way no assertion on `head` alone detects.

That is exactly what `assert cur == start[1:]` is for: it compares the two
passes' idea of the world at the moment they should agree, and fires at build
time rather than corrupting an answer three functions later.
:::

:::check
*Count Connected Components* gives `n` and an edge list. Your build derives the
vertex set from the edges, and your component count is wrong. By how much, and in
which direction?
--
It is too small, by exactly the number of vertices that appear in no edge. Each
of those is a component of size one in the true answer and does not exist at all
in yours.

The direction identifies the bug from the wrong answer alone: too few components,
with dense tests passing, means isolated vertices were dropped; too many usually
means the opposite mistake — a 1-indexed input read into an `n + 1` array,
leaving a phantom vertex 0 that is isolated by construction. The fix is not
defensive coding but discipline: `n` comes from the statement's parameter, never
from `max(edge) + 1`.
:::

:::check
You are given a weighted graph and you store weights in a dictionary
`w[(u, v)]` alongside a plain adjacency list. Name two ways this breaks, and say
what to store instead.
--
First, it cannot represent parallel edges. Two roads between the same pair of
cities with different tolls collapse to whichever was written last, and if the
problem does not promise a simple graph you have silently changed the input.

Second, it costs a tuple allocation and a hash on every relaxation. Dijkstra
touches each half-edge once, so that is `2m` hashes added to a loop whose body is
otherwise a comparison and a heap push — a constant factor large enough to matter
at `m = 10^5`.

Store the weight in the row: `adj[u].append((v, w))`, so it arrives with the
neighbour and costs nothing to find. For the flat version, keep a second array
`wt` parallel to `head`, indexed identically. This is the layout
[[dijkstra]] expects.
:::

:::check
A grid problem gives a `1000 × 1000` board and asks for the shortest path between
two cells. A colleague starts by building an adjacency list with a vertex per
cell. Is that wrong?
--
Not wrong, but it costs a million list objects and up to four million entries for
information the coordinates already imply: every neighbour is `(r±1, c)` or
`(r, c±1)`.

Use the implicit representation — a `neighbours(cell)` function, with visited
marks in a `1000 × 1000` array rather than a set of tuples. The traversal code is
identical, which is the point: an algorithm written against "give me the
neighbours of `u`" does not care where they come from.

Materialising becomes right when the neighbour rule stops being cheap or local,
or when you need the graph in a form the rule cannot give you, such as its
transpose. See [[grid-bfs]].
:::
